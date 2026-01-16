from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.crm import ContactCreate, ContactRead, ContactUpdate, ContactSummary
from app.services.contact_service import ContactService

router = APIRouter()

@router.post("/", response_model=ContactRead)
async def create_contact(
    data: ContactCreate,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    return await ContactService.create(db, tenant_id, data)

@router.get("/", response_model=List[ContactRead])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    return await ContactService.get_all(db, tenant_id, skip, limit)

@router.get("/{contact_id}/summary", response_model=ContactSummary)
async def get_contact_summary(
    contact_id: str,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    return await ContactService.get_summary(db, tenant_id, contact_id)

@router.put("/{contact_id}", response_model=ContactRead)
async def update_contact(
    contact_id: str,
    data: ContactUpdate,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    return await ContactService.update(db, tenant_id, contact_id, data)

@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: str,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    await ContactService.delete(db, tenant_id, contact_id)
    return {"status": "success"}
