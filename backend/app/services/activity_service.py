from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity import ActivityType
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.activity import Activity
from app.models.contact import Contact
from app.schemas.crm import ActivityCreate

class ActivityService:
    @staticmethod
    async def create(db: AsyncSession, tenant_id: str, user_id: str, data: ActivityCreate) -> Activity:
        # Verify Contact
        stmt = select(Contact).where(
            Contact.id == data.contact_id,
            Contact.tenant_id == tenant_id
        )
        result = await db.execute(stmt)
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Contact not found")

        activity = Activity(
            **data.model_dump(),
            tenant_id=tenant_id,
            user_id=user_id
        )
        db.add(activity)
        await db.commit()
        await db.refresh(activity)
        return activity

    @staticmethod
    async def get_by_contact(
        db: AsyncSession, 
        tenant_id: str, 
        contact_id: str, 
        skip: int = 0, 
        limit: int = 50,
        type_: Optional[ActivityType] = None
    ) -> List[Activity]:
        stmt = select(Activity).where(
            Activity.contact_id == contact_id,
            Activity.tenant_id == tenant_id
        )
        
        if type_:
            stmt = stmt.where(Activity.type == type_)
            
        stmt = stmt.order_by(Activity.created_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(stmt)
        return result.scalars().all()
