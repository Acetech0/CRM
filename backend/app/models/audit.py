import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Index, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class AuditLog(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action = Column(String, nullable=False) # e.g. "contact.created"
    
    entity_type = Column(String, nullable=True) # e.g. "contact"
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    
    metadata_ = Column("metadata", JSON, nullable=True) # "metadata" is reserved sometimes
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Tenant Scope
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    
    # User Scope (Nullable, as public actions might not have a user)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)

    __table_args__ = (
        Index('ix_audit_tenant_created', 'tenant_id', 'created_at'),
    )
