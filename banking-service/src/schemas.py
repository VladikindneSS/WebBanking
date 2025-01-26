from pydantic import BaseModel
from datetime import datetime

class AccountCreate(BaseModel):
    pass

class AccountResponse(BaseModel):
    account_number: str
    balance: float

    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    amount: float
    type: str

class TransactionResponse(BaseModel):
    amount: float
    type: str
    timestamp: datetime

    class Config:
        from_attributes = True

class BalanceResponse(BaseModel):
    balance: float