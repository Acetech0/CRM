from typing import Optional
from pydantic import BaseModel, EmailStr, constr

# Shared properties
class TenantBase(BaseModel):
    name: str
    slug: constr(to_lower=True, min_length=3, strip_whitespace=True)

class TenantCreate(TenantBase):
    pass

class TenantRead(TenantBase):
    id: str  # Pydantic handles UUID -> str conversion usually, but explicitly typing str is safe for APIs
    is_active: bool

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: str = "member"

class UserRead(UserBase):
    id: str
    tenant_id: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True

# Auth Payloads
class AuthRegister(BaseModel):
    company_name: str
    company_slug: constr(to_lower=True, min_length=3, strip_whitespace=True)
    admin_email: EmailStr
    admin_password: str
    admin_name: str

class AuthLogin(BaseModel):
    email: EmailStr
    password: str
    tenant_slug: str
