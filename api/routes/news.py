from fastapi import APIRouter, HTTPException
from api.services.news import fetch_latest_news, send_news_digest
from api.schemas.news import NewsResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, BackgroundTasks
import logging


news_router = APIRouter(prefix="/news_digest", tags=['News Digest'])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@news_router.get("/tick")
async def trigger_news_digest(background_tasks: BackgroundTasks, payload: dict):
    """
    Telex calls this endpoint at the specified cron interval to trigger the news digest.
    It receives settings from Telex, extracts the news categories, and runs the digest in the background.
    """
    try:
        settings = payload.get("settings", [])
        categories = next((s["default"] for s in settings if s["label"] == "categories"), None)
        
        if not categories:
            raise HTTPException(status_code=400, detail="Missing 'categories' setting in request payload.")

        logging.info("Received tick request. Categories: %s", categories)

        background_tasks.add_task(send_news_digest, categories)
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({
                "status_code": 200,
                "success": True,
                "message": "News digest generation initiated."
            }
        ))
    except Exception as e:
        logging.error(f"Error processing tick request: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )



@news_router.get("/current_news", response_model=NewsResponse)
def current_news(category: str = "business"):
    data = fetch_latest_news(category)
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({
            "status_code": 200,
            "success": True,
            "message": "Articles fetched successfully",
            "data": data["articles"]
        }
    ))
