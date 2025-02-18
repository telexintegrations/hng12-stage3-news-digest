# main.py
from fastapi import FastAPI
from api.routes import news
from api.core.config import Config

app = FastAPI(
    title=Config.PROJECT_NAME,
    version=Config.PROJECT_VERSION,
    description=Config.PROJECT_DESCRIPTION
)

app.include_router(news.router)
