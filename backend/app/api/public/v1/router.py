from fastapi import APIRouter
from app.api.public.v1.endpoints import leads

api_router = APIRouter()
api_router.include_router(leads.router, prefix="/leads", tags=["public-leads"])
