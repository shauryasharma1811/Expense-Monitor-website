"""Tests for OAuth redirect and callback endpoints with mocked flow/token exchange."""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal, Base, engine
from app.models.models import User, SheetConfig
from app.auth.auth import get_password_hash
from app.google_integration.oauth_service import _state_store

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_oauth_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = db.query(User).filter(User.username == "oauthuser").first()
    if not user:
        user = User(id="user-oauth-1", username="oauthuser", password_hash=get_password_hash("password123"))
        db.add(user)
        db.commit()
    db.close()
    yield
    _state_store.clear()

def test_google_oauth_redirect_and_callback_flow():
    # 1. Login to get token
    login_res = client.post("/api/auth/login", data={"username": "oauthuser", "password": "password123"})
    assert login_res.status_code == 200
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get OAuth redirect URL
    res = client.get("/api/auth/oauth/google", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "authorization_url" in data
    assert len(_state_store) == 1
    state_token = list(_state_store.keys())[0]

    # 3. Test callback with mocked Flow fetch_token
    mock_credentials = MagicMock()
    mock_credentials.token = "fake-access-token"
    mock_credentials.refresh_token = "fake-refresh-token"

    with patch("app.google_integration.oauth_service.Flow") as MockFlow:
        instance = MockFlow.from_client_config.return_value
        instance.fetch_token.return_value = None
        instance.credentials = mock_credentials

        cb_res = client.get(f"/api/auth/oauth/google/callback?code=testcode&state={state_token}")
        assert cb_res.status_code == 200
        assert cb_res.json()["status"] == "success"

    # Verify SheetConfig stored encrypted token
    db = SessionLocal()
    cfg = db.query(SheetConfig).filter(SheetConfig.user_id == "user-oauth-1").first()
    assert cfg is not None
    assert cfg.access_token is not None
    db.close()

def test_oauth_callback_invalid_state():
    res = client.get("/api/auth/oauth/google/callback?code=testcode&state=nonexistentstate")
    assert res.status_code == 400
