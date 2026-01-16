from typing import Any, Dict
from pydantic import BaseModel
from uuid import UUID

class SubmissionCreate(BaseModel):
    form_id: UUID
    data: Dict[str, Any]

class SubmissionResponse(BaseModel):
    id: UUID
    message: str
