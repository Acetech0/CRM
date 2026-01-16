from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.limiter import limiter
from app.core.logging import setup_logging

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# CORS Configuration
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # React default
    "http://localhost:8000",  # Self
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# State & Middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from app.core.errors import global_exception_handler
app.add_exception_handler(Exception, global_exception_handler)

@app.on_event("startup")
async def startup():
    setup_logging()
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

# Placeholder for Include Routers
from app.api.v1.router import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

from app.api.public.v1.router import api_router as public_router
app.include_router(public_router, prefix="/public/v1")

from app.api import health
app.include_router(health.router, tags=["health"])

@app.get("/")
def root():
    return {"message": "Welcome to Mini CRM API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
