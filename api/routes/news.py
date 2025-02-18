from fastapi import APIRouter
from api.services.news import fetch_latest_news, send_news_digest
from api.schemas.news import NewsResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, BackgroundTasks


router = APIRouter()


@router.get("/news_digest")
async def trigger_news_digest(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_news_digest)
    return {"message": "News digest generation initiated."}


@router.get("/current_news", response_model=NewsResponse)
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
