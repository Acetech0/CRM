import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Website(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain = Column(String, index=True, nullable=False)
    name = Column(String, nullable=True)
    tracking_id = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Ownership
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False, index=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="websites")
    forms = relationship("Form", back_populates="website")
    contacts = relationship("Contact", back_populates="website")

    __table_args__ = (
        UniqueConstraint('tenant_id', 'domain', name='uq_website_tenant_domain'),
    )
