from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from .database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://auth-service:8063/auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        with open("public.pem") as f:
            public_key = f.read()
            
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="banking-service"
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )