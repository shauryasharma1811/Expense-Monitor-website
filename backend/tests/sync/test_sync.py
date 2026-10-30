"""Tests for sync worker with mocked Google Sheets API responses."""
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, Base, engine
from app.models.models import User, SheetConfig, Expense
from app.auth.auth import get_password_hash
from app.google_integration.crypto import encrypt_token, decrypt_token
from app.sync.sync_worker import sync_user_sheet


@pytest.fixture(autouse=True)
def setup_sync_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = db.query(User).filter(User.username == "syncuser").first()
    if not user:
        user = User(id="user-sync-1", username="syncuser", password_hash=get_password_hash("password123"))
        db.add(user)
        db.commit()
    else:
        db.rollback()
    # Ensure SheetConfig exists for syncuser
    cfg = db.query(SheetConfig).filter(SheetConfig.user_id == "user-sync-1").first()
    if not cfg:
        cfg = SheetConfig(
            id="cfg-1",
            user_id="user-sync-1",
            spreadsheet_id="mock-sheet-id",
            sheet_name="Sheet1",
            access_token=encrypt_token("mock_access_token"),
            refresh_token=encrypt_token("mock_refresh_token"),
        )
        db.add(cfg)
        db.commit()
    db.close()
    yield
    # Cleanup
    db = SessionLocal()
    db.query(Expense).filter(Expense.user_id == "user-sync-1").delete()
    db.commit()
    db.close()


def test_sync_worker_reads_and_writes_expenses():
    """Mock Google Sheets service; verify sync_user_sheet writes Expense rows."""
    mock_service = MagicMock()
    mock_values = mock_service.spreadsheets().values().get().execute
    mock_values.return_value = {
        "values": [
            ["RowID", "Date", "Description", "Category", "Amount", "Currency", "Status"],
            ["TXN-101", "2026-10-30", "Cloud Hosting", "Infrastructure", "99.99", "USD", "completed"],
        ]
    }

    with patch("app.sync.sync_worker.get_google_sheets_service", return_value=mock_service):
        db = SessionLocal()
        count = sync_user_sheet(db, "user-sync-1")
        db.close()

    assert count == 1

    db = SessionLocal()
    expenses = db.query(Expense).filter(Expense.user_id == "user-sync-1").all()
    assert len(expenses) >= 1
    assert any(exp.description == "Cloud Hosting" for exp in expenses)
    db.close()


def test_sync_worker_diff_updates_existing_row():
    """Mock sheet with updated amount; verify Expense is updated, not duplicated."""
    db = SessionLocal()
    exp = Expense(
        id="exp-existing",
        user_id="user-sync-1",
        sheet_row_id="TXN-101",
        date="2026-10-30",
        description="Old Description",
        amount="10.00",
        category="Test",
        currency="USD",
        status="completed",
    )
    db.add(exp)
    db.commit()
    db.close()

    mock_service = MagicMock()
    mock_service.spreadsheets().values().get().execute.return_value = {
        "values": [
            ["RowID", "Date", "Description", "Category", "Amount", "Currency", "Status"],
            ["TXN-101", "2026-10-30", "Updated Description", "Test", "55.50", "USD", "completed"],
        ]
    }

    with patch("app.sync.sync_worker.get_google_sheets_service", return_value=mock_service):
        db = SessionLocal()
        count = sync_user_sheet(db, "user-sync-1")
        db.close()

    assert count == 1
    db = SessionLocal()
    updated = db.query(Expense).filter(Expense.id == "exp-existing").first()
    assert updated is not None
    assert updated.description == "Updated Description"
    assert float(updated.amount) == 55.50
    db.close()


def test_sync_worker_missing_config():
    db = SessionLocal()
    count = sync_user_sheet(db, "nonexistent-user")
    db.close()
    assert count == 0
