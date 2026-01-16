from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, constr, Field

# Shared properties
class TenantBase(BaseModel):
    name: str
    slug: constr(to_lower=True, min_length=3, strip_whitespace=True)

class TenantCreate(TenantBase):
    pass

class TenantRead(TenantBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=64)
    role: str = "member"

class UserRead(UserBase):
    id: UUID
    tenant_id: UUID
    is_active: bool
    role: str

    class Config:
        from_attributes = True

# Auth Payloads
class AuthRegister(BaseModel):
    company_name: str
    company_slug: constr(to_lower=True, min_length=3, strip_whitespace=True)
    admin_email: EmailStr
    admin_password: str = Field(..., min_length=8, max_length=64)
    admin_name: str

class AuthLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)
    tenant_slug: str
