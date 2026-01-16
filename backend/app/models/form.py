import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base

class Form(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    # schema column removed in favor of form_fields table
    settings = Column(JSONB, default={}, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Ownership
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False, index=True)
    website_id = Column(UUID(as_uuid=True), ForeignKey("website.id"), nullable=False, index=True)
    
    # Relationships
    tenant = relationship("Tenant")
    website = relationship("Website", back_populates="forms")
    fields = relationship("FormField", back_populates="form", cascade="all, delete-orphan", order_by="FormField.order")
