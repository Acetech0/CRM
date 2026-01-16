from fastapi import Request, status
from fastapi.responses import JSONResponse
import traceback
import logging

logger = logging.getLogger("api")

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Exception: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc), "trace": traceback.format_exc().splitlines()},
    )
