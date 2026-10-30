"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings
from app.api import api_router

app = FastAPI(title="Expense Monitor API")

# Configure CORS for local development origins (frontend & Swagger)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Health check has no authentication requirement for simplicity
@app.get("/api/health")
async def health() -> dict:
    settings = Settings()
    return {"status": "ok", "version": settings.APP_VERSION}
