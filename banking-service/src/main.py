from fastapi import FastAPI
from .database import engine, Base
from .routers import accounts, transactions, health

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Banking Service")

app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(health.router)