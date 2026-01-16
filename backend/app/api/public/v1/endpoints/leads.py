from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api import deps
from app.core.limiter import limiter
from app.schemas.public import PublicLeadCreate
from app.schemas.crm import ContactCreate
from app.models.tenant import Tenant
from app.services.contact_service import ContactService

router = APIRouter()

@router.post("/leads")
@limiter.limit("5/minute")
async def create_public_lead(
    request: Request,
    data: PublicLeadCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(deps.get_db)
):
    # 1. Resolve Tenant by Slug (No JWT)
    stmt = select(Tenant).where(Tenant.slug == data.tenant_slug)
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        # Security: Return 404 to avoid enumeration? 
        # Or 400? 404 feels safer or just "Success" to pretend.
        # For now, explicit error for developer debug.
        raise HTTPException(status_code=404, detail="Tenant not found")
        
    # 2. Convert to ContactCreate
    contact_data = ContactCreate(
        name=data.name,
        email=data.email,
        phone=data.phone,
        source=data.source,
        status="new"
    )
    
    # 3. Create Contact (Triggers Audit Log via BackgroundTasks)
    # user_id is None because it's public
    contact = await ContactService.create(
        db, 
        tenant_id=str(tenant.id), 
        data=contact_data, 
        background_tasks=background_tasks
    )
    
    return {"status": "success", "id": str(contact.id)}
