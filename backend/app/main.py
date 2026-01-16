from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Placeholder for Include Routers
from app.api.v1.router import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to Mini CRM API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
