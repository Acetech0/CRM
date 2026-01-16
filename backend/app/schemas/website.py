from typing import Optional
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime

class WebsiteBase(BaseModel):
    domain: str = Field(..., min_length=4, max_length=255, description="Domain name (e.g. example.com)")
    name: Optional[str] = Field(None, max_length=100, description="Friendly name")

class WebsiteCreate(WebsiteBase):
    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v: str) -> str:
        return v.lower().strip()

class WebsiteResponse(WebsiteBase):
    id: UUID
    tracking_id: str
    is_active: bool
    created_at: datetime
    tenant_id: UUID

    class Config:
        from_attributes = True
