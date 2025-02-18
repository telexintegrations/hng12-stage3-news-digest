from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
import logging
from api.core.config import Config
from api.services.news import generate_news_digest

telex_router = APIRouter(prefix="/telex", tags=['Telex'])


@telex_router.get("/integration.json")
async def get_integration_json(request: Request):
    """
    Exposes the integration.json endpoint.
    """
    base_url = str(request.base_url).rstrip("/")
    INTEGRATION_JSON = {
        "data": {
            "date": {
                "created_at": "2025-02-18",
                "updated_at": "2025-02-18"
            },
            "descriptions": {
                "app_name": "News Digest",
                "app_description": "An automated news digest service that fetches and summarizes news articles from multiple sources, then sends the digest to Telex.",
                "app_logo": "https://github.com/Ayobamidele/hng12-stage3-news-digest/blob/main/assets/news_digest.jpg",
                "app_url": base_url,
                "background_color": "#fff"
            },
            "is_active": True,
            "integration_type": "interval",
            "key_features": [
                "Fetches news from multiple categories",
                "Uses AI summarization for digest generation",
                "Sends digest to Telex channels"
            ],
            "integration_category": "Communication & Collaboration",
            "author": "Ayobamidele Ewetuga",
            "website": base_url,
            "settings": [
                {
                    "label": "categories",
                    "type": "text",
                    "required": True,
                    "default": "business,technology,sports,health,entertainment"
                },
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "0 */6 * * * "
                }
            ],
            "target_url": "",
            "tick_url": f"{base_url}/api/v1/news_digest/tick"
        }
    }
    return INTEGRATION_JSON
