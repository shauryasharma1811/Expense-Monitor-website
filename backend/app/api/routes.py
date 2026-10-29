from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.models.schemas import UserLogin, TokenResponse, ExpensesResponse, SyncStatusInfo, RefreshResponse
from app.auth.auth import verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/auth/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check if default user exists, if not create one for testing
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"token": access_token, "user": {"username": user.username}}

@router.get("/expenses", response_model=ExpensesResponse)
async def get_expenses(
    page: int = 1,
    page_size: int = 20,
    search: str = "",
    date_from: str | None = None,
    date_to: str | None = None,
    sort_by: str = "date",
    sort_order: str = "desc",
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Stub implementation returning sample data complying with contract
    sample_data = [
        {
            "id": "1",
            "transactionId": "TXN-001",
            "date": "2026-10-25",
            "description": "AWS Cloud Hosting",
            "category": "Infrastructure",
            "amount": 1250.00,
            "currency": "USD",
            "status": "completed"
        },
        {
            "id": "2",
            "transactionId": "TXN-002",
            "date": "2026-10-28",
            "description": "Office Supplies",
            "category": "Operations",
            "amount": 340.50,
            "currency": "USD",
            "status": "completed"
        }
    ]
    return {"data": sample_data, "total": len(sample_data), "totalPages": 1}

@router.post("/expenses/refresh", response_model=RefreshResponse)
async def refresh_expenses(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {"refreshed": True, "count": 2}

@router.get("/sync-status", response_model=SyncStatusInfo)
async def get_sync_status(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {"status": "connected", "lastSync": "2026-10-30T10:00:00Z", "message": "Successfully synced with Google Sheets"}

@router.get("/auth/oauth/google")
async def google_oauth_redirect():
    return {"auth_url": "https://accounts.google.com/o/oauth2/auth?client_id=placeholder"}

@router.get("/auth/oauth/google/callback")
async def google_oauth_callback(code: str):
    return {"token": "sample-oauth-token", "sheet_id": "sample-sheet-id"}
