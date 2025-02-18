from fastapi import APIRouter
from api.routes.news import news_router
from api.routes.telex import telex_router

api_version_one = APIRouter(prefix="/api/v1")

api_version_one.include_router(news_router, tags=["News"])
api_version_one.include_router(telex_router, tags=["Telex"])