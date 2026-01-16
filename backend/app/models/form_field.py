import uuid
import enum
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base

class FieldType(str, enum.Enum):
    TEXT = "text"
    EMAIL = "email"
    NUMBER = "number"
    TEXTAREA = "textarea"
    SELECT = "select"
    CHECKBOX = "checkbox"

class FormField(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identifiers
    key = Column(String, nullable=False) # e.g. "email"
    label = Column(String, nullable=False) # e.g. "Email Address"
    
    # Config
    field_type = Column(Enum(FieldType), nullable=False)
    required = Column(Boolean, default=False)
    order = Column(Integer, default=0)
    options = Column(JSONB, nullable=True) # For select/radio
    placeholder = Column(String, nullable=True)
    
    # Ownership
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    form_id = Column(UUID(as_uuid=True), ForeignKey("form.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Relationships
    form = relationship("Form", back_populates="fields")
