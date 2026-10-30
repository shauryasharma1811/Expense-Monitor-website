"""Google OAuth service for redirect and callback with in-memory state validation."""
from urllib.parse import urlencode
import secrets

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from app.core.config import Settings
from app.google_integration.crypto import encrypt_token, decrypt_token
from app.models.models import SheetConfig

settings = Settings()

# Placeholder client credentials — never use real secrets
CLIENT_ID = "placeholder-google-client-id.apps.googleusercontent.com"
CLIENT_SECRET = "placeholder-google-client-secret"

# Minimal scopes for spreadsheet access
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly",
         "https://www.googleapis.com/auth/spreadsheets"]

# Temporary in-memory state store for this exercise
_state_store: dict[str, dict] = {}


def generate_state(user_id: str) -> str:
    state_token = secrets.token_urlsafe(32)
    _state_store[state_token] = {"user_id": user_id}
    return state_token


def validate_state(state_token: str, user_id: str) -> bool:
    entry = _state_store.get(state_token)
    if entry is None:
        return False
    return entry.get("user_id") == user_id


def build_auth_redirect_url(user_id: str, redirect_uri: str) -> str:
    state_token = generate_state(user_id)
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri],
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = redirect_uri
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
        state=state_token,
    )
    return authorization_url


def handle_oauth_callback(code: str, state: str, redirect_uri: str) -> dict:
    entry = _state_store.get(state)
    if not entry or "user_id" not in entry:
        raise ValueError("Invalid or missing state parameter")
    user_id = entry["user_id"]
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri],
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = redirect_uri
    flow.fetch_token(code=code)
    credentials = flow.credentials
    # Encrypt tokens server-side before persisting
    access_token_enc = encrypt_token(credentials.token)
    refresh_token_enc = encrypt_token(credentials.refresh_token) if credentials.refresh_token else None
    return {
        "user_id": user_id,
        "access_token_enc": access_token_enc,
        "refresh_token_enc": refresh_token_enc,
        "token_expiry": getattr(credentials, "expiry", None),
    }


def build_sheets_service(access_token: str):
    """Build a Google Sheets service with server-side token."""
    credentials = type("Creds", (), {
        "token": access_token,
        "refresh_token": None,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scopes": SCOPES,
    })()
    service = build("sheets", "v4", credentials=credentials)
    return service
