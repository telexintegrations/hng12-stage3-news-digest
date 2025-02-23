from fastapi import APIRouter, Request

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
                "updated_at": "2025-02-22"
            },
            "descriptions": {
                "app_name": "News Digest",
                "app_description": "An automated news digest service that fetches and summarizes news articles from multiple sources, then sends the digest to Telex.",
                "app_logo": "https://ucarecdn.com/ca598933-5ebc-49c8-a338-d7fef3bed1df/news_digest.jpg",
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
                    "type": "multi-select",
                    "description": "select categories to filter trending news",
                    "options": ["business","technology","sports","health","entertainment"],
                    "default": ["technology", "business"]
                },
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "* * * * *"
                }
            ],
            "target_url": "",
            "tick_url": f"{base_url}/api/v1/news_digest/tick"
        }
    }
    return INTEGRATION_JSON
