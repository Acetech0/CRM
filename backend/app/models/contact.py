import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class ContactStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    LOST = "lost"

class Contact(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    source = Column(String, nullable=True) # e.g. "website", "referral"
    
    status = Column(Enum(ContactStatus), default=ContactStatus.NEW, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Tenant Scope
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)

    # Relationships
    # deals = relationship("Deal", back_populates="contact")
    # activities = relationship("Activity", back_populates="contact")

    # Composite Index for fast lookups by tenant
    __table_args__ = (
        Index('ix_contact_tenant_email', 'tenant_id', 'email'),
        Index('ix_contact_tenant_created', 'tenant_id', 'created_at'),
    )
