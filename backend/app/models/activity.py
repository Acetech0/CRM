import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class ActivityType(str, enum.Enum):
    CALL = "call"
    EMAIL = "email"
    NOTE = "note"
    MEETING = "meeting"
    FORM = "form"

class Activity(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(ActivityType), default=ActivityType.NOTE, nullable=False)
    content = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Tenant Scope
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False, index=True)
    
    # Relationships
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contact.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)

    __table_args__ = (
        Index('ix_activity_tenant_created', 'tenant_id', 'created_at'),
    )
