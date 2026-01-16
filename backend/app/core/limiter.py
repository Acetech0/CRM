from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

def get_tenant_user_key(request: Request) -> str:
    """
    Custom key builder for Rate Limiting.
    If authenticated, limit by (Tenant + User).
    If public, limit by IP.
    """
    # This logic relies on Request.state which we might populate in middleware
    # Or strict IP fallback for now.
    return get_remote_address(request)

limiter = Limiter(key_func=get_remote_address)
