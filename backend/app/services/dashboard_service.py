from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.contact import Contact
from app.models.deal import Deal, DealStage

class DashboardService:
    @staticmethod
    async def get_overview_stats(db: AsyncSession, tenant_id: str):
        # 1. Total Contacts
        stmt_contacts = select(func.count(Contact.id)).where(Contact.tenant_id == tenant_id)
        result_contacts = await db.execute(stmt_contacts)
        total_contacts = result_contacts.scalar() or 0

        # 2. Active Deals (Not Won or Lost)
        stmt_active_deals = select(func.count(Deal.id)).where(
            Deal.tenant_id == tenant_id,
            Deal.stage.notin_([DealStage.WON, DealStage.LOST])
        )
        result_active = await db.execute(stmt_active_deals)
        active_deals = result_active.scalar() or 0

        # 3. Pipeline Value (Sum of Active Deals)
        stmt_value = select(func.sum(Deal.value)).where(
            Deal.tenant_id == tenant_id,
            Deal.stage.notin_([DealStage.WON, DealStage.LOST])
        )
        result_value = await db.execute(stmt_value)
        pipeline_value = result_value.scalar() or 0

        # 4. Won vs Lost
        stmt_won = select(func.count(Deal.id)).where(Deal.tenant_id == tenant_id, Deal.stage == DealStage.WON)
        result_won = await db.execute(stmt_won)
        won_count = result_won.scalar() or 0

        stmt_lost = select(func.count(Deal.id)).where(Deal.tenant_id == tenant_id, Deal.stage == DealStage.LOST)
        result_lost = await db.execute(stmt_lost)
        lost_count = result_lost.scalar() or 0

        return {
            "total_contacts": total_contacts,
            "active_deals": active_deals,
            "pipeline_value": float(pipeline_value) if pipeline_value else 0.0,
            "won_count": won_count,
            "lost_count": lost_count
        }

    @staticmethod
    async def get_pipeline_breakdown(db: AsyncSession, tenant_id: str):
        # Group by Stage
        stmt = select(Deal.stage, func.count(Deal.id)).where(
            Deal.tenant_id == tenant_id
        ).group_by(Deal.stage)
        
        result = await db.execute(stmt)
        data = result.all()
        
        # Convert to dictionary with defaults
        breakdown = {stage.value: 0 for stage in DealStage}
        for stage, count in data:
            breakdown[stage.value] = count
            
        return breakdown
