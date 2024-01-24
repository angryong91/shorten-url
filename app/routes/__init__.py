from fastapi import APIRouter

from app.routes import short

api_router = APIRouter()
api_router.include_router(short.router, prefix="/shorts", tags=["short"])
