from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class PublicLeadCreate(BaseModel):
    tenant_slug: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    source: str = "public_form"
