from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.deal import Deal
from app.models.contact import Contact
from app.schemas.crm import DealCreate, DealUpdate, DealStage

class DealService:
    @staticmethod
    async def create(db: AsyncSession, tenant_id: str, data: DealCreate) -> Deal:
        # Verify Contact exists in THIS tenant
        stmt = select(Contact).where(
            Contact.id == data.contact_id,
            Contact.tenant_id == tenant_id
        )
        result = await db.execute(stmt)
        contact = result.scalar_one_or_none()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found in this tenant")

        deal = Deal(
            **data.model_dump(),
            tenant_id=tenant_id
        )
        db.add(deal)
        await db.commit()
        await db.refresh(deal)
        return deal

    @staticmethod
    async def get_all(db: AsyncSession, tenant_id: str) -> List[Deal]:
        stmt = select(Deal).where(Deal.tenant_id == tenant_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_stage(db: AsyncSession, tenant_id: str, deal_id: str, stage: DealStage) -> Deal:
        stmt = select(Deal).where(
            Deal.id == deal_id,
            Deal.tenant_id == tenant_id
        )
        result = await db.execute(stmt)
        deal = result.scalar_one_or_none()
        
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
            
        deal.stage = stage
        await db.commit()
        await db.refresh(deal)
        return deal

    @staticmethod
    async def update(db: AsyncSession, tenant_id: str, deal_id: str, data: DealUpdate) -> Deal:
        stmt = select(Deal).where(Deal.id == deal_id, Deal.tenant_id == tenant_id)
        deal = (await db.execute(stmt)).scalar_one_or_none()
        
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
            
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(deal, key, value)
            
        db.add(deal)
        await db.commit()
        await db.refresh(deal)
        return deal

    @staticmethod
    async def delete(db: AsyncSession, tenant_id: str, deal_id: str):
        stmt = select(Deal).where(Deal.id == deal_id, Deal.tenant_id == tenant_id)
        deal = (await db.execute(stmt)).scalar_one_or_none()
        
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
            
        await db.delete(deal)
        await db.commit()
