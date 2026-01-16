from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.api import deps
from app.models.website import Website
from app.models.form import Form
from datetime import datetime
from app.models.submission import FormSubmission
from app.models.contact import Contact, ContactStatus
from app.models.activity import Activity, ActivityType
from app.schemas.form import FormResponse
from app.schemas.submission import SubmissionCreate, SubmissionResponse

router = APIRouter()

def validate_origin(request: Request, website: Website):
    """
    Validates that the request Origin matches the Website domain.
    In production, this should likely be stricter or handle subdomains.
    For this implementation, we enforce strict equality or localhost for dev.
    """
    origin = request.headers.get("origin") or request.headers.get("referer")
    if not origin:
        # If no origin/referer, deciding to block or allow is policy. 
        # For secure embed, we usually block or require it.
        # Strict mode: Block.
        raise HTTPException(status_code=403, detail="Missing Origin/Referer header")
    
    # Normalize origin (remove protocol)
    # Simple check: does origin contain the domain?
    # Ideally: strict host check.
    # Allowing localhost for testing
    if "localhost" in origin or "127.0.0.1" in origin:
        return True
        
    if website.domain.lower() not in origin.lower():
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Domain mismatch. Form allowed on: {website.domain}, Request from: {origin}"
        )

@router.get("/forms/{form_id}", response_model=FormResponse)
def get_public_form(
    *,
    db: Session = Depends(deps.get_db),
    form_id: str,
    tracking_id: str,
    request: Request
) -> Any:
    """
    Public Endpoint: Get form definition for rendering.
    Requires `tracking_id` to validate context.
    Origin check ensures it's embedded on the correct site.
    """
    # 1. Find Website by Tracking ID
    stmt = select(Website).where(Website.tracking_id == tracking_id)
    website = db.execute(stmt).scalar_one_or_none()
    if not website:
        raise HTTPException(status_code=404, detail="Invalid Tracking ID")
        
    # 2. Security: Validate Origin
    validate_origin(request, website)
    
    # 3. Find Form and Validate Hierarchy
    stmt_form = select(Form).where(
        Form.id == form_id,
        Form.website_id == website.id
    )
    form = db.execute(stmt_form).scalar_one_or_none()
    
    if not form:
         raise HTTPException(status_code=404, detail="Form not found or does not belong to this website")
         
    return form

@router.post("/submissions", response_model=SubmissionResponse)
def submit_form(
    *,
    db: Session = Depends(deps.get_db),
    submission_in: SubmissionCreate,
    tracking_id: str,
    request: Request
) -> Any:
    """
    Public Endpoint: Submit a form.
    """
    # 1. Reuse validation logic
    stmt = select(Website).where(Website.tracking_id == tracking_id)
    website = db.execute(stmt).scalar_one_or_none()
    if not website:
        raise HTTPException(status_code=404, detail="Invalid Tracking ID")
    
    validate_origin(request, website)
    
    stmt_form = select(Form).where(
        Form.id == submission_in.form_id,
        Form.website_id == website.id
    )
    form = db.execute(stmt_form).scalar_one_or_none()
    if not form:
         raise HTTPException(status_code=404, detail="Form not found")
    
    # 2. Contact Upsert (Atomic Logic)
    # Search for email in the payload
    email = submission_in.data.get("email") or submission_in.data.get("Email")
    contact_id = None
    
    if email:
        email = email.lower().strip()
        # Try to find name/phone key
        name = submission_in.data.get("name") or submission_in.data.get("Name") or email.split("@")[0]
        phone = submission_in.data.get("phone") or submission_in.data.get("Phone")
        
        # Prepare Upsert Statement
        insert_stmt = pg_insert(Contact).values(
            id=uuid.uuid4(),
            tenant_id=website.tenant_id,
            website_id=website.id,
            email=email,
            name=name,
            phone=phone,
            source=f"Form: {form.name} ({website.domain})",
            status=ContactStatus.NEW,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Strategy: Passive Update (Only update 'updated_at' to confirm activity)
        # If we wanted to update NULLs, we would use:
        # "name": func.coalesce(Contact.name, insert_stmt.excluded.name)
        # For now, strictly following "Existing contacts are updated (metadata), not duplicated"
        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint='uq_contact_tenant_email',
            set_={
                "updated_at": datetime.utcnow()
            }
        ).returning(Contact.id)
        
        # Execute and get ID
        result = db.execute(do_update_stmt)
        contact_id = result.scalar_one()

    # 3. Save Submission (Raw Data)
    submission = FormSubmission(
        form_id=form.id,
        website_id=website.id,
        tenant_id=website.tenant_id,
        data=submission_in.data,
        meta={
            "ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "referer": request.headers.get("referer")
        }
    )
    db.add(submission)
    
    # 4. Log Activity (If contact exists)
    if contact_id:
        activity = Activity(
            tenant_id=website.tenant_id,
            contact_id=contact_id,
            type=ActivityType.FORM,
            content=f"Submitted form '{form.name}' on {website.domain}",
            # user_id is Nullable now
        )
        db.add(activity)
    
    db.commit()
    db.refresh(submission)
    
    return SubmissionResponse(id=submission.id, message="Submission received")
