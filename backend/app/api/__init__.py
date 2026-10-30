from fastapi import APIRouter
from app.api.routes import router as api_routes
from app.google_integration.auth import router as google_auth_router
from app.auth.auth import auth_router

api_router = APIRouter()
api_router.include_router(api_routes)
api_router.include_router(google_auth_router)
api_router.include_router(auth_router)
