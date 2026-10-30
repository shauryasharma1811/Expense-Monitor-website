from sqlalchemy import Column, String, DateTime, Numeric, Text, ForeignKey, func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SheetConfig(Base):
    __tablename__ = "sheet_configs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    spreadsheet_id = Column(String, nullable=False)
    sheet_name = Column(String, default="Sheet1")
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    sheet_row_id = Column(String, unique=True, index=True, nullable=False)
    date = Column(String, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="completed")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(String, primary_key=True, index=True)
    token = Column(Text, unique=True, index=True, nullable=False)
    revoked_at = Column(DateTime(timezone=True), server_default=func.now())
