from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_version_one
from api.core.config import Config

app = FastAPI(
    title=Config.PROJECT_NAME,
    version=Config.PROJECT_VERSION,
    description=Config.PROJECT_DESCRIPTION
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://staging.telextest.im", "http://telextest.im", "https://staging.telex.im", "https://telex.im", "https://ping.telex.im", "https://newsapi.org", "https://generativelanguage.googleapis.com"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)
app.include_router(api_version_one)
