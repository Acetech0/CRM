from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.models.contact import ContactStatus
from app.models.deal import DealStage
from app.models.activity import ActivityType

# --- Contact Schemas ---
class ContactBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: ContactStatus = ContactStatus.NEW

from uuid import UUID

class ContactCreate(ContactBase):
    website_id: Optional[UUID] = None

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: Optional[ContactStatus] = None

class ContactRead(ContactBase):
    id: str
    tenant_id: str
    created_at: str

    class Config:
        from_attributes = True


# --- Deal Schemas ---
class DealBase(BaseModel):
    title: str
    value: float = 0
    stage: DealStage = DealStage.LEAD

class DealCreate(DealBase):
    contact_id: str

class DealUpdate(BaseModel):
    title: Optional[str] = None
    value: Optional[float] = None
    stage: Optional[DealStage] = None

class DealStageUpdate(BaseModel):
    stage: DealStage

class DealRead(DealBase):
    id: str
    tenant_id: str
    contact_id: str
    created_at: str

    class Config:
        from_attributes = True


# --- Activity Schemas ---
class ActivityBase(BaseModel):
    type: ActivityType
    content: Optional[str] = None

class ActivityCreate(ActivityBase):
    contact_id: str

class ActivityUpdate(BaseModel):
    content: Optional[str] = None
    type: Optional[ActivityType] = None

class ActivityRead(ActivityBase):
    id: str
    tenant_id: str
    contact_id: str
    user_id: str
    created_at: str

    class Config:
        from_attributes = True

# --- Composite Summaries ---
class ContactSummary(BaseModel):
    contact: ContactRead
    deals: List[DealRead]
    recent_activities: List[ActivityRead]
    activity_count: int
    total_pipeline_value: float
