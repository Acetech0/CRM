from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.api import deps

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Checks if the application is running and can connect to the database.
    Used by Load Balancers (e.g. Render, AWS ALB).
    """
    health_status = {"status": "ok", "database": "unknown", "cache": "unknown"}
    
    # 1. Check Database
    try:
        await db.execute(text("SELECT 1"))
        health_status["database"] = "connected"
    except Exception as e:
        health_status["database"] = "unreachable"
        health_status["status"] = "error"
        # Log error in production
        print(f"Health Check DB Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Database unreachable"
        )
        
    # 2. Check Cache (Optional - if using Redis)
    # import fastapi_cache
    # if fastapi_cache.FastAPICache.get_backend():
    #     ...
    
    return health_status
