import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, Base, engine
from app.models.models import User, Expense
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

def test_get_expenses_unauthorized():
    response = client.get("/api/expenses")
    assert response.status_code == 401

def test_get_expenses_authorized():
    login_res = client.post("/api/auth/login", data={"username": "bankemployee", "password": "securepassword"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/expenses", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total" in data
    assert "totalPages" in data

def test_refresh_expenses():
    login_res = client.post("/api/auth/login", data={"username": "bankemployee", "password": "securepassword"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/expenses/refresh", headers=headers)
    assert response.status_code == 200
    assert response.json()["refreshed"] is True

def test_sync_status():
    login_res = client.post("/api/auth/login", data={"username": "bankemployee", "password": "securepassword"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/sync-status", headers=headers)
    assert response.status_code == 200
    assert "status" in response.json()
