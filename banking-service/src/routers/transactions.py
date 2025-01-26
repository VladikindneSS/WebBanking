from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..dependencies import get_db, verify_token

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=schemas.TransactionResponse)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(verify_token)
):
    account = db.query(models.Account).filter(
        models.Account.user_id == token_payload.get("sub")
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    new_transaction = models.Transaction(
        amount=transaction.amount,
        type=transaction.type,
        account_id=account.id
    )
    
    if transaction.type == "credit":
        account.balance += transaction.amount
    elif transaction.type == "debit":
        if account.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        account.balance -= transaction.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return new_transaction

@router.post("/transfer")
async def transfer_funds(
    recipient_account: str,
    amount: float,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(verify_token)
):
    sender_account = db.query(models.Account).filter(
        models.Account.user_id == token_payload.get("sub")
    ).first()
    
    recipient = db.query(models.Account).filter(
        models.Account.account_number == recipient_account
    ).first()
    
    if not sender_account or not recipient:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if sender_account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Дебетовая транзакция для отправителя
    sender_transaction = models.Transaction(
        amount=amount,
        type="debit",
        account_id=sender_account.id
    )
    
    # Кредитная транзакция для получателя
    recipient_transaction = models.Transaction(
        amount=amount,
        type="credit",
        account_id=recipient.id
    )
    
    sender_account.balance -= amount
    recipient.balance += amount
    
    db.add_all([sender_transaction, recipient_transaction])
    db.commit()
    
    return {"message": "Transfer successful"}