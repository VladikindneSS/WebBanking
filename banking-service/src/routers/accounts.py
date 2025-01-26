from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..dependencies import get_db, verify_token

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post(
    "/create",
    response_model=schemas.AccountResponse,
    summary="Create new account",
    description="Generates a unique account number for the logged-in user."
)
async def create_account(
    db: Session = Depends(get_db),
    token_payload: dict = Depends(verify_token)
):
    # Получаем user_id из токена
    user_id = int(token_payload["sub"])
    
    # Генерируем уникальный номер счёта
    account_number = utils.generate_account_number()

    # Проверяем, чтобы номер был уникален
    while db.query(models.Account).filter(models.Account.account_number == account_number).first():
        account_number = utils.generate_account_number()

    # Создаём новый счёт
    new_account = models.Account(
        account_number=account_number,
        user_id=user_id,  # Привязываем счёт к текущему пользователю
        balance=0.0
    )
    
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    return new_accoun

@router.get(
    "/",
    response_model=List[schemas.AccountResponse],
    summary="Get all accounts for the logged-in user",
    description="Returns all accounts associated with the currently logged-in user."
)
async def get_accounts(
    db: Session = Depends(get_db),
    token_payload: dict = Depends(verify_token)  # Проверяем токен и получаем payload
):
    # Получаем user_id из токена
    user_id = int(token_payload["sub"])
    
    # Извлекаем счета, привязанные к user_id
    accounts = db.query(models.Account).filter(models.Account.user_id == user_id).all()
    
    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No accounts found for the user."
        )
    
    return accounts