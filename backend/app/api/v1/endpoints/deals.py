from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.crm import DealCreate, DealRead
from app.services.deal_service import DealService

router = APIRouter()

@router.post("/", response_model=DealRead)
async def create_deal(
    data: DealCreate,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    return await DealService.create(db, tenant_id, data)

@router.get("/", response_model=List[DealRead])
async def read_deals(
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    return await DealService.get_all(db, tenant_id)
