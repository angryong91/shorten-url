from app.routes import short
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(short.router, prefix="/shorts", tags=["short"])
