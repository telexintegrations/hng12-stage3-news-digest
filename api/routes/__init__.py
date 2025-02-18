from fastapi import APIRouter
from api.routes.news import news_router

api_version_one = APIRouter(prefix="/api/v1")

api_version_one.include_router(news_router, tags=["News"])