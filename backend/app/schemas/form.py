from typing import Optional, List, Literal, Any
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime

class FormFieldBase(BaseModel):
    key: str = Field(..., min_length=1, pattern="^[a-zA-Z0-9_]+$")
    label: str
    field_type: Literal["text", "email", "number", "textarea", "select", "checkbox"]
    required: bool = False
    order: int = 0
    options: Optional[List[str]] = None
    placeholder: Optional[str] = None

class FormFieldCreate(FormFieldBase):
    pass

class FormFieldResponse(FormFieldBase):
    id: UUID

    class Config:
        from_attributes = True

class FormCreate(BaseModel):
    name: str
    settings: dict = {}
    fields: List[FormFieldCreate]

    @field_validator('fields')
    @classmethod
    def validate_unique_keys(cls, v):
        keys = [f.key for f in v]
        if len(keys) != len(set(keys)):
            raise ValueError("Field keys must be unique within the form")
        return v

class FormResponse(BaseModel):
    id: UUID
    name: str
    website_id: UUID
    settings: dict
    created_at: datetime
    fields: List[FormFieldResponse]

    class Config:
        from_attributes = True
