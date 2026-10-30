from pydantic import BaseModel
from typing import Optional, List

class ExpenseRecord(BaseModel):
    id: str
    transactionId: str
    date: str
    description: str
    category: str
    amount: float
    currency: str = "USD"
    status: Optional[str] = "completed"

    class Config:
        from_attributes = True

class ExpensesResponse(BaseModel):
    data: List[ExpenseRecord]
    total: int
    totalPages: int

class SyncStatusInfo(BaseModel):
    status: str
    lastSync: Optional[str] = None
    message: Optional[str] = None

class RefreshResponse(BaseModel):
    refreshed: bool
    count: int

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str
    user: dict
