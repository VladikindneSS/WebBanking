from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src import models, schemas, dependencies

router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/token", response_model=schemas.TokenResponse)
async def login(
    email: str, 
    password: str,
    db: Session = Depends(dependencies.get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    with open("private.pem") as f:
        private_key = f.read()

    access_token = jwt.encode(
        {
            "sub": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iss": "auth-service",
            "aud": "banking-service"
        },
        private_key,
        algorithm="RS256"
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.UserResponse)
async def register(
    user: schemas.UserCreate,
    db: Session = Depends(dependencies.get_db)
):
    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) | 
        (models.User.phone == user.phone)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone already registered"
        )
    
    hashed_password = pwd_context.hash(user.password)
    
    new_user = models.User(
        email=user.email,
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user