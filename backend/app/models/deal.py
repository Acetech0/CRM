import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class DealStage(str, enum.Enum):
    LEAD = "lead"
    PROPOSAL = "proposal"
    WON = "won"
    LOST = "lost"

class Deal(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    value = Column(Numeric, default=0)
    stage = Column(Enum(DealStage), default=DealStage.LEAD, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Tenant Scope
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False, index=True)
    
    # Relationships
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contact.id"), nullable=False, index=True)
    # contact = relationship("Contact", back_populates="deals")

    __table_args__ = (
        Index('ix_deal_tenant_created', 'tenant_id', 'created_at'),
    )
