from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.schemas.auth import AuthRegister, AuthLogin, UserRead
from app.schemas.token import Token
from app.models.tenant import Tenant
from app.models.user import User, UserRole
from app.core import security
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register(
    data: AuthRegister,
    db: AsyncSession = Depends(get_db)
):
    # 1. Check if Tenant slug exists
    stmt = select(Tenant).where(Tenant.slug == data.company_slug)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Tenant slug already exists."
        )

    # 2. Atomic Transaction: Create Tenant + Admin User
    try:
        # Create Tenant
        new_tenant = Tenant(
            name=data.company_name,
            slug=data.company_slug
        )
        db.add(new_tenant)
        await db.flush()  # To get new_tenant.id

        # Create Admin User
        hashed_password = security.get_password_hash(data.admin_password)
        new_user = User(
            email=data.admin_email,
            password_hash=hashed_password,
            full_name=data.admin_name,
            role=UserRole.ADMIN,
            tenant_id=new_tenant.id
        )
        db.add(new_user)
        
        await db.commit()
        await db.refresh(new_user)
        return new_user
        
    except Exception as e:
        await db.rollback()
        # In production, log the actual error
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(
    data: AuthLogin,
    db: AsyncSession = Depends(get_db)
):
    # 1. Resolve Tenant
    stmt = select(Tenant).where(Tenant.slug == data.tenant_slug)
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(status_code=400, detail="Tenant not found")
        
    if not tenant.is_active:
        raise HTTPException(status_code=400, detail="Tenant is inactive")

    # 2. Find User in THIS Tenant
    # Notice Strict Scoping: We ONLY look for users with matching tenant_id
    stmt = select(User).where(
        User.email == data.email,
        User.tenant_id == tenant.id
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not security.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is inactive")

    # 3. Issue Token with Tenant Context
    access_token = security.create_access_token(
        subject=user.id,
        tenant_id=str(tenant.id)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
