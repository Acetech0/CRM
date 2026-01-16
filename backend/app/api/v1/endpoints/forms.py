from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.api import deps
from app.models.form import Form
from app.models.form_field import FormField
from app.models.website import Website
from app.schemas.form import FormCreate, FormResponse
from app.models.user import User
from app.models.submission import FormSubmission
from sqlalchemy import select, func, desc
from fastapi.responses import StreamingResponse
import io
import csv
import uuid

router = APIRouter()

@router.post("/websites/{website_id}/forms", response_model=FormResponse)
def create_form(
    *,
    db: Session = Depends(deps.get_db),
    website_id: uuid.UUID,
    form_in: FormCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create a new form with fields for a specific website.
    """
    # 1. Verify Website ownership
    stmt = select(Website).where(
        Website.id == website_id,
        Website.tenant_id == current_user.tenant_id
    )
    website = db.execute(stmt).scalar_one_or_none()
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website not found or access denied"
        )
    
    # 2. Create Form
    form = Form(
        name=form_in.name,
        settings=form_in.settings,
        website_id=website_id,
        tenant_id=current_user.tenant_id
    )
    db.add(form)
    db.flush() # Get form.id
    
    # 3. Create Fields
    for field_in in form_in.fields:
        field = FormField(
            form_id=form.id,
            tenant_id=current_user.tenant_id,
            key=field_in.key,
            label=field_in.label,
            field_type=field_in.field_type,
            required=field_in.required,
            order=field_in.order,
            options=field_in.options,
            placeholder=field_in.placeholder
        )
        db.add(field)
    
    db.commit()
    db.refresh(form)
    return form

@router.get("/forms/{form_id}", response_model=FormResponse)
def get_form(
    *,
    db: Session = Depends(deps.get_db),
    form_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get form details.
    """
    stmt = select(Form).where(
        Form.id == form_id,
        Form.tenant_id == current_user.tenant_id
    )
    form = db.execute(stmt).scalar_one_or_none()
    
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
        
    return form

@router.get("/forms/{form_id}/stats")
def get_form_stats(
    *,
    db: Session = Depends(deps.get_db),
    form_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get aggregated stats for a form.
    """
    # Verify access
    stmt = select(Form).where(Form.id == form_id, Form.tenant_id == current_user.tenant_id)
    if not db.execute(stmt).scalar_one_or_none():
         raise HTTPException(status_code=404, detail="Form not found")

    # Stats Query
    submission_count = db.query(func.count(FormSubmission.id)).filter(FormSubmission.form_id == form_id).scalar()
    last_submission = db.query(func.max(FormSubmission.created_at)).filter(FormSubmission.form_id == form_id).scalar()
    
    return {
        "submission_count": submission_count,
        "last_submission": last_submission
    }

@router.get("/forms/{form_id}/submissions")
def get_form_submissions(
    *,
    db: Session = Depends(deps.get_db),
    form_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get submissions list.
    """
    # Verify access
    stmt = select(Form).where(Form.id == form_id, Form.tenant_id == current_user.tenant_id)
    if not db.execute(stmt).scalar_one_or_none():
         raise HTTPException(status_code=404, detail="Form not found")
         
    submissions = db.query(FormSubmission)\
        .filter(FormSubmission.form_id == form_id)\
        .order_by(desc(FormSubmission.created_at))\
        .offset(skip)\
        .limit(limit)\
        .all()
        
    return submissions

@router.get("/forms/{form_id}/export")
def export_form_submissions(
    *,
    db: Session = Depends(deps.get_db),
    form_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Export submissions to CSV.
    """
    # Verify access
    stmt = select(Form).where(Form.id == form_id, Form.tenant_id == current_user.tenant_id)
    form = db.execute(stmt).scalar_one_or_none()
    if not form:
         raise HTTPException(status_code=404, detail="Form not found")
         
    submissions = db.query(FormSubmission)\
        .filter(FormSubmission.form_id == form_id)\
        .order_by(desc(FormSubmission.created_at))\
        .limit(1000)\
        .all() # Cap at 1000 for safety in MVP

    # Generate CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers logic
    headers = ["Submission ID", "Date", "IP Address"]
    
    # Dynamic headers from data keys
    keys = set()
    for sub in submissions:
        if sub.data:
            keys.update(sub.data.keys())
    sorted_keys = sorted(list(keys))
    headers.extend(sorted_keys)
    
    writer.writerow(headers)
    
    for sub in submissions:
        row = [str(sub.id), sub.created_at.isoformat(), sub.meta.get("ip", "") if sub.meta else ""]
        for key in sorted_keys:
            row.append(sub.data.get(key, ""))
        writer.writerow(row)
        
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=form_export_{form_id}.csv"}
    )
