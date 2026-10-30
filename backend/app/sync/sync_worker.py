from sqlalchemy.orm import Session
from app.models.models import SheetConfig, Expense
from app.google_integration.sheets_service import get_google_sheets_service, fetch_spreadsheet_rows
from decimal import Decimal, InvalidOperation
import logging
import secrets

logger = logging.getLogger(__name__)

def sync_user_sheet(db: Session, user_id: str) -> int:
    """
    Syncs expenses for a specific user from their connected Google Spreadsheet.
    Diffs incoming rows against the database and inserts/updates accordingly.
    Returns the count of synced/updated expense records.
    """
    sheet_config = db.query(SheetConfig).filter(SheetConfig.user_id == user_id).first()
    if not sheet_config or not sheet_config.access_token:
        logger.warning(f"No valid SheetConfig or access token found for user {user_id}")
        return 0

    try:
        service = get_google_sheets_service(sheet_config.access_token, sheet_config.refresh_token)
        rows = fetch_spreadsheet_rows(service, sheet_config.spreadsheet_id, f"{sheet_config.sheet_name}!A:G")
    except Exception as e:
        logger.error(f"Failed to fetch spreadsheet rows for user {user_id}: {e}")
        # If testing or using mock service when real API fails, fallback or re-raise
        rows = []

    if not rows or len(rows) <= 1:
        # No rows or only header row
        return 0

    header = rows[0]
    data_rows = rows[1:]

    synced_count = 0
    for idx, row in enumerate(data_rows):
        if len(row) < 6:
            continue

        # Expected row format: [RowID, Date, Description, Category, Amount, Currency, Status] (or similar)
        # We map flexibly by header or indices:
        # 0: sheet_row_id or transactionId, 1: date, 2: description, 3: category, 4: amount, 5: currency, 6: status
        try:
            sheet_row_id = str(row[0]) if len(row) > 0 else f"row-{idx}"
            date_str = str(row[1]) if len(row) > 1 else "2026-10-30"
            description = str(row[2]) if len(row) > 2 else "No description"
            category = str(row[3]) if len(row) > 3 else "General"

            raw_amount = str(row[4]) if len(row) > 4 else "0.00"
            amount = Decimal(raw_amount.replace("$", "").replace(",", ""))

            currency = str(row[5]) if len(row) > 5 else "USD"
            status = str(row[6]) if len(row) > 6 else "completed"
        except (IndexError, ValueError, InvalidOperation) as err:
            logger.warning(f"Skipping malformed row {idx}: {row} error: {err}")
            continue

        # Diff check against Expense table
        existing_expense = db.query(Expense).filter(
            Expense.user_id == user_id,
            Expense.sheet_row_id == sheet_row_id
        ).first()

        if existing_expense:
            # Update if changed
            updated = False
            if existing_expense.date != date_str:
                existing_expense.date = date_str
                updated = True
            if existing_expense.description != description:
                existing_expense.description = description
                updated = True
            if existing_expense.category != category:
                existing_expense.category = category
                updated = True
            if existing_expense.amount != amount:
                existing_expense.amount = amount
                updated = True
            if existing_expense.currency != currency:
                existing_expense.currency = currency
                updated = True
            if existing_expense.status != status:
                existing_expense.status = status
                updated = True

            if updated:
                db.add(existing_expense)
                synced_count += 1
        else:
            # Insert new expense record
            new_expense = Expense(
                id=secrets.token_hex(8),
                user_id=user_id,
                sheet_row_id=sheet_row_id,
                date=date_str,
                description=description,
                category=category,
                amount=amount,
                currency=currency,
                status=status
            )
            db.add(new_expense)
            synced_count += 1

    db.commit()
    return synced_count

def sync_all_active_sheets(db: Session) -> int:
    """
    Syncs sheets for all users with configurations.
    """
    configs = db.query(SheetConfig).all()
    total_synced = 0
    for cfg in configs:
        count = sync_user_sheet(db, cfg.user_id)
        total_synced += count
    return total_synced
