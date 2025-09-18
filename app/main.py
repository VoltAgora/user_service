from fastapi import FastAPI
from app.adapters.http.routes import router as user_router

app = FastAPI(title="User Service")

app.include_router(user_router, prefix="/user")