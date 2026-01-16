from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.crm import DealCreate, DealRead, DealStageUpdate, DealUpdate
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

@router.put("/{deal_id}/stage", response_model=DealRead)
async def update_deal_stage(
    deal_id: str,
    data: DealStageUpdate,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    return await DealService.update_stage(db, tenant_id, deal_id, data.stage)

@router.put("/{deal_id}", response_model=DealRead)
async def update_deal(
    deal_id: str,
    data: DealUpdate,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    return await DealService.update(db, tenant_id, deal_id, data)

@router.delete("/{deal_id}")
async def delete_deal(
    deal_id: str,
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    await DealService.delete(db, tenant_id, deal_id)
    return {"status": "success"}
