from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog
from app.db.session import AsyncSessionLocal

class AuditService:
    @staticmethod
    async def log_event(
        tenant_id: str,
        action: str,
        user_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Logs an event to the database.
        Designed to be run in a background task (Create new session).
        """
        async with AsyncSessionLocal() as db:
            audit = AuditLog(
                tenant_id=tenant_id,
                action=action,
                user_id=user_id,
                entity_type=entity_type,
                entity_id=entity_id,
                metadata_=metadata
            )
            db.add(audit)
            await db.commit()
