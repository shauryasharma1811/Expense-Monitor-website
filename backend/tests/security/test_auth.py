import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, Base, engine
from app.models.models import User
from app.auth.auth import get_password_hash

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(User).filter(User.username == "bankemployee").first():
        user = User(id="1", username="bankemployee", password_hash=get_password_hash("securepassword"))
        db.add(user)
        db.commit()
    db.close()
    yield

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_login_success():
    response = client.post("/api/auth/login", data={"username": "bankemployee", "password": "securepassword"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure():
    response = client.post("/api/auth/login", data={"username": "bankemployee", "password": "wrongpassword"})
    assert response.status_code == 400

def test_missing_token_access():
    # Access protected endpoint without token should return 401
    response = client.get("/api/expenses")
    assert response.status_code == 401

def test_expired_token_behavior():
    # Create an expired token manually and verify 401
    from app.auth.auth import create_access_token
    from datetime import timedelta
    expired_token = create_access_token({"sub": "bankemployee"}, expires_delta=timedelta(minutes=-1))
    response = client.get("/api/expenses", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401

def test_rate_limit_enforcement():
    # Try 6 failed attempts to exceed 5 per hour (using fresh IP attempts via direct rate limit)
    # We reset attempts by importing module directly
    from app.auth.auth import login_attempts
    login_attempts.clear()
    # 5 allowed attempts with wrong password should pass as 400, 6th should be 429
    for i in range(5):
        r = client.post("/api/auth/login", data={"username": "bankemployee", "password": "bad"})
        assert r.status_code == 400
    # 6th attempt should hit rate limit
    r = client.post("/api/auth/login", data={"username": "bankemployee", "password": "bad"})
    assert r.status_code == 429
