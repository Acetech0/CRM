from datetime import datetime, timedelta
from typing import Optional, Any, Union
import jwt
import bcrypt
from app.core.config import settings

def _prepare_password(password: str) -> bytes:
    """
    Prepare password for bcrypt:
    1. Encode to UTF-8
    2. Truncate to 72 bytes (bcrypt's hard limit)
    
    This ensures we never crash on long passwords.
    """
    return password.encode("utf-8")[:72]

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt.checkpw expects both arguments to be bytes
    try:
        return bcrypt.checkpw(
            _prepare_password(plain_password),
            hashed_password.encode("utf-8")
        )
    except ValueError:
        # Handle cases where hashed_password might be invalid formatting
        return False

def get_password_hash(password: str) -> str:
    # salt is generated automatically by gensalt
    pwd_bytes = _prepare_password(password)
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

def create_access_token(subject: Union[str, Any], tenant_id: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"sub": str(subject), "tenant_id": tenant_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
