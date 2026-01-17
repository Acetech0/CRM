from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.website import Website
from app.schemas.website import WebsiteCreate, WebsiteResponse
from app.models.user import User
import uuid

router = APIRouter()

@router.get("/", response_model=List[WebsiteResponse])
async def read_websites(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve websites.
    """
    stmt = select(Website).where(Website.tenant_id == current_user.tenant_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    websites = result.scalars().all()
    return websites

@router.post("/", response_model=WebsiteResponse)
async def create_website(
    *,
    db: AsyncSession = Depends(deps.get_db),
    website_in: WebsiteCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Register a new website.
    """
    # 1. Check uniqueness within tenant
    stmt = select(Website).where(
        Website.tenant_id == current_user.tenant_id,
        Website.domain == website_in.domain
    )
    existing_website = (await db.execute(stmt)).scalar_one_or_none()
    
    if existing_website:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This domain is already registered for your account."
        )

    # 2. Generate Tracking ID
    # Use a simple prefix + random hex for readability and uniqueness
    tracking_id = f"TRK-{uuid.uuid4().hex[:12].upper()}"
    
    # 3. Create Object
    website = Website(
        domain=website_in.domain,
        name=website_in.name,
        tracking_id=tracking_id,
        tenant_id=current_user.tenant_id
    )
    
    db.add(website)
    await db.commit()
    await db.refresh(website)
    
    return website
