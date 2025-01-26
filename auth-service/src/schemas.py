from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    surname: str
    phone: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    phone: str

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str