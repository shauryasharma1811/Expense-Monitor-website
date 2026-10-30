"""FastAPI router for Google OAuth endpoints (/auth/oauth/google and /auth/oauth/google/callback)."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import SheetConfig, User
from app.auth.auth import get_current_user
from app.google_integration.oauth_service import build_auth_redirect_url, handle_oauth_callback, validate_state

router = APIRouter(prefix="/auth/oauth/google", tags=["Google OAuth"])


@router.get("")
async def oauth_google_redirect(request: Request, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Initiate Google OAuth flow, returning redirect URL."""
    user_record = db.query(User).filter(User.username == current_user["username"]).first()
    if not user_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    base_url = str(request.base_url).rstrip("/")
    redirect_uri = f"{base_url}/api/auth/oauth/google/callback"
    auth_url = build_auth_redirect_url(user_record.id, redirect_uri)
    return {"authorization_url": auth_url}


@router.get("/callback")
async def oauth_google_callback(code: str, state: str, request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth callback, exchange code for tokens, encrypt and store."""
    base_url = str(request.base_url).rstrip("/")
    redirect_uri = f"{base_url}/api/auth/oauth/google/callback"

    # Validate state using the temporary in-memory dict (service-level)
    from app.google_integration.oauth_service import _state_store
    if not state or state not in _state_store:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state parameter")
    try:
        token_info = handle_oauth_callback(code=code, state=state, redirect_uri=redirect_uri)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    user_id = token_info["user_id"]
    # Save or update SheetConfig securely
    config = db.query(SheetConfig).filter(SheetConfig.user_id == user_id).first()
    if not config:
        config = SheetConfig(
            id=f"cfg_{user_id}",
            user_id=user_id,
            spreadsheet_id="default-spreadsheet-id",
            access_token=token_info["access_token_enc"],
            refresh_token=token_info["refresh_token_enc"]
        )
        db.add(config)
    else:
        config.access_token = token_info["access_token_enc"]
        if token_info["refresh_token_enc"]:
            config.refresh_token = token_info["refresh_token_enc"]
    db.commit()

    return {"status": "success", "message": "Google account successfully linked and tokens stored securely."}
