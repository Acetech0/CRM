import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class WebhookSubscription(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, nullable=False)
    secret = Column(String, nullable=False) # Hmac secret
    events = Column(JSON, nullable=False) # List of events ["contact.created"]
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Tenant Scope
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
