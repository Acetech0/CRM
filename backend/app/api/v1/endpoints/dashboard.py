from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from app.api import deps
from app.services.dashboard_service import DashboardService

router = APIRouter()

@router.get("/overview")
@cache(expire=60)
async def get_overview(
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    """
    Returns high-level CRM metrics:
    - Total Contacts
    - Active Deals Count
    - Pipeline Value (Sum of active deals)
    - Won / Lost Counts
    """
    return await DashboardService.get_overview_stats(db, tenant_id)

@router.get("/pipeline")
@cache(expire=60)
async def get_pipeline_breakdown(
    db: AsyncSession = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_current_tenant_id)
):
    """
    Returns deal counts grouped by stage:
    { "lead": 10, "proposal": 5, "won": 2, "lost": 8 }
    """
    return await DashboardService.get_pipeline_breakdown(db, tenant_id)
