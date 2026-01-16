from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.crm import ActivityCreate, ActivityRead
from app.models.activity import ActivityType
from app.models.user import User
from app.services.activity_service import ActivityService

router = APIRouter()

@router.post("/", response_model=ActivityRead)
async def create_activity(
    data: ActivityCreate,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id),
    current_user: User = Depends(deps.get_current_user)
):
    return await ActivityService.create(db, tenant_id, str(current_user.id), data)

@router.get("/{contact_id}", response_model=List[ActivityRead])
async def read_activities(
    contact_id: str,
    skip: int = 0,
    limit: int = 50,
    type: Optional[ActivityType] = None,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    return await ActivityService.get_by_contact(db, tenant_id, contact_id, skip=skip, limit=limit, type_=type)
