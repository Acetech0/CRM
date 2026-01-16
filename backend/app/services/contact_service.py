from typing import List, Optional
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.contact import Contact
from app.models.deal import Deal
from app.models.activity import Activity
from app.schemas.crm import ContactCreate, ContactUpdate, ContactSummary
from app.services.audit_service import AuditService
from app.models.website import Website
import uuid

class ContactService:
    @staticmethod
    async def get(db: AsyncSession, tenant_id: str, contact_id: str) -> Optional[Contact]:
        stmt = select(Contact).where(
            Contact.id == contact_id,
            Contact.tenant_id == tenant_id
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession, tenant_id: str, skip: int = 0, limit: int = 100) -> List[Contact]:
        stmt = select(Contact).where(
            Contact.tenant_id == tenant_id
        ).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create(
        db: AsyncSession, 
        tenant_id: str, 
        data: ContactCreate,
        background_tasks: Optional[BackgroundTasks] = None,
        user_id: Optional[str] = None
    ) -> Contact:
        website_id = data.website_id
        
        # Logic: If no website provided (Manual), use Tenant's System Website
        if not website_id:
            stmt = select(Website).where(
                Website.tenant_id == tenant_id,
                Website.is_system == True
            )
            system_site = (await db.execute(stmt)).scalar_one_or_none()
            
            # Fallback: Create if somehow missing
            if not system_site:
                print(f"⚠️ System Website missing for tenant {tenant_id}. Creating lazily.")
                system_site = Website(
                    domain=f"internal.{tenant_id}.crm",
                    name="System Internal",
                    tenant_id=tenant_id,
                    is_system=True,
                    tracking_id=f"SYS-{uuid.uuid4().hex[:8].upper()}"
                )
                db.add(system_site)
                await db.flush()
            
            website_id = system_site.id
            if not data.source:
                data.source = "manual"
        
        else:
            # Verify Website ownership
            stmt = select(Website).where(Website.id == website_id, Website.tenant_id == tenant_id)
            if not (await db.execute(stmt)).scalar_one_or_none():
                 raise HTTPException(400, "Invalid Website ID for this tenant")

        contact = Contact(
            **data.model_dump(exclude={"website_id"}), # Exclude to avoid double logic
            tenant_id=tenant_id,
            website_id=website_id
        )
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        
        if background_tasks:
            # Async Audit Log
            background_tasks.add_task(
                AuditService.log_event,
                tenant_id=tenant_id,
                action="contact.created",
                user_id=user_id,
                entity_type="contact",
                entity_id=str(contact.id),
                metadata={"name": contact.name, "source": contact.source}
            )
            
        return contact

    @staticmethod
    async def update(db: AsyncSession, tenant_id: str, contact_id: str, data: ContactUpdate) -> Contact:
        contact = await ContactService.get(db, tenant_id, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
            
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(contact, key, value)
            
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        return contact

    @staticmethod
    async def get_summary(db: AsyncSession, tenant_id: str, contact_id: str) -> ContactSummary:
        # 1. Get Contact
        contact = await ContactService.get(db, tenant_id, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
            
        # 2. Get Recent Activities (Limit 5)
        stmt_act = select(Activity).where(
            Activity.contact_id == contact_id,
            Activity.tenant_id == tenant_id
        ).order_by(Activity.created_at.desc()).limit(5)
        activities = (await db.execute(stmt_act)).scalars().all()
        
        # 3. Get Active Deals & Pipeline Value
        stmt_deals = select(Deal).where(
            Deal.contact_id == contact_id,
            Deal.tenant_id == tenant_id
        )
        deals = (await db.execute(stmt_deals)).scalars().all()
        
        # 4. Aggregates (Count activities)
        stmt_count = select(func.count(Activity.id)).where(
            Activity.contact_id == contact_id,
            Activity.tenant_id == tenant_id
        )
        act_count = (await db.execute(stmt_count)).scalar() or 0
        
        pipeline_value = sum(d.value for d in deals)
        
        return {
            "contact": contact,
            "deals": deals,
            "recent_activities": activities,
            "activity_count": act_count,
            "total_pipeline_value": float(pipeline_value)
        }

    @staticmethod
    async def delete(db: AsyncSession, tenant_id: str, contact_id: str):
        contact = await ContactService.get(db, tenant_id, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        await db.delete(contact)
        await db.commit()
