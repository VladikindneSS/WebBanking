from sqlalchemy import Column, Integer, String
from src.database import Base

class User(Base):
    __tablename__ = "users"  # Указание имени таблицы

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    phone = Column(String, unique=True)
    hashed_password = Column(String)