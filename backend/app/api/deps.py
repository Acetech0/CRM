from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core import security
from app.core.config import settings
from app.schemas.token import TokenPayload
from app.db.session import get_db
from app.models.user import User, UserRole  # Added Import

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

async def get_current_user_context(
    token: str = Depends(reusable_oauth2)
) -> TokenPayload:
    """
    Decodes the JWT and returns the payload (User ID + Tenant ID).
    Does NOT query the DB yet (stateless validation for speed).
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data

async def get_current_tenant_id(
    token_data: TokenPayload = Depends(get_current_user_context)
) -> str:
    """
    Extracts tenant_id from the validated token.
    This can be injected into Services/Repositories to enforce isolation.
    """
    if not token_data.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token missing tenant context",
        )
    return token_data.tenant_id

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token_data: TokenPayload = Depends(get_current_user_context)
) -> User:
    """
    Fetches the current user from the Database.
    CRITICAL: Validates that the user belongs to the tenant claims in the token.
    """
    from app.models.user import User  # Late import to avoid cycles
    
    # 1. We start with the user ID from the token
    user_id = token_data.sub
    tenant_id = token_data.tenant_id
    
    if not user_id or not tenant_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # 2. Strict Tenant Scoping:
    # We MUST filter by BOTH id AND tenant_id.
    # If a user ID exists but in a different tenant, this query returns None.
    stmt = select(User).where(
        User.id == user_id,
        User.tenant_id == tenant_id
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="User not found in this tenant context"
        )
        
    if not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user")
         
    return user

async def get_current_active_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifies that the current user is an admin.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="The user does not have enough privileges"
        )
    return current_user

def require_role(required_roles: list[UserRole]):
    """
    Factory for a dependency that checks if the user has one of the required roles.
    """
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Role {current_user.role} does not have sufficient permissions"
            )
        return current_user
    return role_checker
