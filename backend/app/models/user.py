import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"
    SALES = "sales"
    VIEWER = "viewer"

class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.MEMBER, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Tenant Relationship
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False, index=True)
    # We can add a relationship back to tenant if needed
    # tenant = relationship("Tenant")

    # Composite Unique Constraint: Email is unique PER TENANT
    __table_args__ = (
        UniqueConstraint('email', 'tenant_id', name='uq_user_email_tenant'),
    )
