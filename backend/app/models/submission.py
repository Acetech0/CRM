import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base

class FormSubmission(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Payload
    data = Column(JSONB, default={}, nullable=False)
    meta = Column(JSONB, default={}, nullable=True) # IP, User-Agent, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Context & Isolation
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False, index=True)
    website_id = Column(UUID(as_uuid=True), ForeignKey("website.id"), nullable=False, index=True)
    form_id = Column(UUID(as_uuid=True), ForeignKey("form.id"), nullable=False, index=True)
    
    # Relationships
    tenant = relationship("Tenant")
    website = relationship("Website")
    form = relationship("Form")
