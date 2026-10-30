"""Main FastAPI application entry point."""

from fastapi import FastAPI
from app.core.config import Settings
from app.api import api_router

app = FastAPI(title="Expense Monitor API")

# Include API routes
app.include_router(api_router, prefix="/api")

# Health check has no authentication requirement for simplicity
@app.get("/api/health")
async def health() -> dict:
    settings = Settings()
    return {"status": "ok", "version": settings.APP_VERSION}
