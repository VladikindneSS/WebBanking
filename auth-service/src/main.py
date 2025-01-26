from fastapi import FastAPI
from .routers import auth, health
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(auth.router)
app.include_router(health.router)