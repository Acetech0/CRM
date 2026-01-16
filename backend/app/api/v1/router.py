from fastapi import APIRouter
from app.api.v1.endpoints import auth, contacts, deals, activities, dashboard, websites, forms, public

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(deals.router, prefix="/deals", tags=["deals"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(websites.router, prefix="/websites", tags=["websites"])
api_router.include_router(forms.router, tags=["forms"])
api_router.include_router(public.router, prefix="/public", tags=["public"]) # Note: mix of top-level and nested routes
