import threading
import requests
import json
import logging
from api.core.config import Config

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
CATEGORIES = ["business", "technology", "sports", "health", "entertainment"]

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting")

def fetch_latest_news(category: str):
    params = {
        'country': Config.NEWS_COUNTRY,
        'apiKey': Config.NEWS_API_KEY,
        "category": category
    }
    response = requests.get(NEWS_API_URL, params=params)
    return response.json()

def retrieve_ai_summarizer(articles):
    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'key': Config.SUMMARIZER_API_KEY,
    }

    prompt = """
        You are tasked with summarizing a list of news articles, each represented as a dictionary. Your output should be a coherent short article that captures the essence of the news stories, including a catchy title that reflects the main theme in less or a bit more than a 1000 words. At the end of the article, provide a reference section that cites each article used in the summary. Do not put a note to all, only some, so it fits within the word range. Also, do not repeat yourself.

        **Instructions:**

        1. **Input Structure**: You will receive a list of dictionaries. Each dictionary contains:
            - `title`: The title of the news article.
            - `content`: A brief description or excerpt of the article.
            - `source`: The source or publication of the article.
            - `date`: The publication date of the article.

        2. **Output Requirements**:
            - **Title**: Create a catchy and engaging title that encapsulates the main idea of the summarized articles.
            - **Article Body**: Write a concise summary that:
                - Integrates key points from all provided articles.
                - Maintains a logical flow and coherent narrative.
                - Uses clear and engaging language suitable for a general audience.
            - **References**: At the end of your article, include a reference section that lists all the articles mentioned in the summary. Each reference should include the title, source, and date of publication.

        3. **Formatting**:
            - Use headings and bullet points where necessary for clarity.
            - Ensure that the references are formatted consistently.

        **Example Input**:
        ```json
        [
            {
                "source": {
                    "id": null,
                    "name": "BBC News"
                },
                "author": null,
                "title": "Kim Sae-ron: South Korean actress found dead, aged 24 - BBC.com",
                "description": "Kim began her career as a child actor and was seen as one of the country's most promising actresses.",
                "url": "https://www.bbc.com/news/articles/c626p25egddo",
                "urlToImage": "https://ichef.bbci.co.uk/news/1024/branded_news/6fd4/live/05338e70-ec6d-11ef-a319-fb4e7360c4ec.jpg",
                "publishedAt": "2025-02-16T15:17:27Z",
                "content": "South Korean actress Kim Sae-ron has been found dead in Seoul, police have said. The 24-year-old was found in her home in the city's Seongsu-dong district by a friend at around 16:55 (07:55 GMT) on … [+943 chars]"
            },
            {
                "source": {
                    "id": null,
                    "name": "CBS Sports"
                },
                "author": null,
                "title": "2025 Daytona 500 props, odds, best bets, expert predictions: Include William Byron in NASCAR parlay picks - CBS Sports",
                "description": "Phil Bobbitt and Steve Greco revealed their NASCAR picks for sites like PrizePicks, Underdog Fantasy, Sleeper Fantasy, and DraftKings Pick6",
                "url": "https://www.cbssports.com/nascar/news/2025-daytona-500-props-odds-best-bets-expert-predictions-include-william-byron-in-nascar-parlay-picks/",
                "urlToImage": "https://sportshub.cbsistatic.com/i/r/2025/02/10/963a8e4c-c0a8-40d7-b78f-010232eb55ba/thumbnail/1200x675/6029b3a8cf2fd097fb242f445847759d/nascar-5-usatsi.jpg",
                "publishedAt": "2025-02-16T15:13:22Z",
                "content": "Denny Hamlin has three Daytona 500 victories, putting him in elite company heading into the 2025 Daytona 500 on Sunday. Jimmie Johnson, who is not locked into the Daytona 500 field, has two wins in t… [+4186 chars]"
            }
        ]
        ```
    """
    json_data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': prompt + "\n" + json.dumps(articles),
                    },
                ],
            },
        ],
    }

    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
        params=params,
        headers=headers,
        json=json_data,
    )

    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]['parts'][0]['text']



def send_news_digest_to_telex(news_articles: list):
    message = retrieve_ai_summarizer(news_articles)
    payload = {
        "message": str(message), 
        "event_name": "News Flash",
        "status": "success",
        "username": "gerald"
    }
    
    response = requests.post(
        Config.TELEX_API_URL,
        json=payload,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    
    if response.status_code == 202:
        logger.info("News digest successfully sent to Telex.")
    else:
        logger.info(f"Failed to send news digest to Telex. Status code: {response.status_code}",)

def generate_news_digest():
    all_articles = []
    for category in CATEGORIES:
        news_data = fetch_latest_news(category)
        if news_data.get("status") == "ok":
            all_articles.extend(news_data.get("articles", []))

    send_news_digest_to_telex(all_articles)

def send_news_digest():
    digest_thread = threading.Thread(target=generate_news_digest)
    digest_thread.start()
    digest_thread.join()
    logger.info("Completed news digest generation and sent to Telex.")
