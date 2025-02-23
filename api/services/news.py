import threading
import requests
import json
import logging
from api.core.config import Config

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
      You are tasked with summarizing a list of news articles, each represented as a dictionary.
      Your output should be a coherent short article that captures the essence of the news stories, including a catchy title that reflects the main theme in **800-1200 words**.
      At the end of the article, provide a reference section that cites each article used in the summary.
      Ensure that references are included for most but not necessarily all articles to maintain conciseness. Avoid repetition in your summary.

        **Instructions:**

        1. **Input Structure**: You will receive a list of dictionaries. Each dictionary contains:
            - `title`: The title of the news article.
            - `content`: A brief description or excerpt of the article.
            - `source`: The source or publication of the article.
            - `date`: The publication date of the article.
            - `url`: The link to the original article.

        2. **Output Requirements**:
            - **Title**: Create a bold, engaging title that encapsulates the main idea of the summarized articles.
            - **Article Body**:
                - Integrate key points from all provided articles.
                - Maintain a logical flow and coherent narrative.
                - Use clear and engaging language suitable for a general audience.
                - Utilize bullet points and lists to emphasize key takeaways.
            - **References**:
                - Include a reference section at the end.
                - Each reference should list the **title, source, date of publication**, and a clickable link in the following format:
                
                ```
                **Title** - Source (Date) 🔗[Link]
                ```
                - Ensure that references are concise and properly formatted, but not all articles need to be referenced if unnecessary.

        3. **Formatting**:
            - Use **bold headings** to separate sections clearly.
            - Bullet points should highlight key facts and statistics.
            - Ensure that the article is structured logically for readability.

        ---

        ### **Example Input:**
        ```json
        [
            {
                "source": { "id": null, "name": "BBC News" },
                "title": "Kim Sae-ron: South Korean actress found dead, aged 24 - BBC.com",
                "description": "Kim began her career as a child actor and was seen as one of the country's most promising actresses.",
                "url": "https://www.bbc.com/news/articles/c626p25egddo",
                "publishedAt": "2025-02-16T15:17:27Z",
                "content": "South Korean actress Kim Sae-ron has been found dead in Seoul, police have said. The 24-year-old was found in her home in the city's Seongsu-dong district by a friend at around 16:55 (07:55 GMT) on …"
            },
            {
                "source": { "id": null, "name": "CBS Sports" },
                "title": "2025 Daytona 500 props, odds, best bets, expert predictions: Include William Byron in NASCAR parlay picks - CBS Sports",
                "description": "Phil Bobbitt and Steve Greco revealed their NASCAR picks for sites like PrizePicks, Underdog Fantasy, Sleeper Fantasy, and DraftKings Pick6",
                "url": "https://www.cbssports.com/nascar/news/2025-daytona-500-props-odds-best-bets-expert-predictions-include-william-byron-in-nascar-parlay-picks/",
                "publishedAt": "2025-02-16T15:13:22Z",
                "content": "Denny Hamlin has three Daytona 500 victories, putting him in elite company heading into the 2025 Daytona 500 on Sunday. Jimmie Johnson, who is not locked into the Daytona 500 field, has two wins in t…"
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
        "username": "Gerald - The News Digest bot "
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

def generate_news_digest(categories: list[str]):
    if not categories:
        logger.warning("No categories provided for news digest generation.")
        return

    for category in categories:
        try:
            news_data = fetch_latest_news(category)
            if news_data.get("status") != "ok":
                logger.error(f"Failed to fetch news for category '{category}': {news_data}")
                continue

            articles = news_data.get("articles", [])
            if not articles:
                logger.warning(f"No articles found for category '{category}'.")
                continue

            send_news_digest_to_telex(articles)
            logger.info(f"Sent {len(articles)} articles from category '{category}' to Telex.")

        except Exception as e:
            logger.exception(f"Error processing category '{category}': {e}")

    logger.info("Completed news digest generation and sent to Telex.")


def send_news_digest(categories: list[str]):
    digest_thread = threading.Thread(target=generate_news_digest, args=(categories,))
    digest_thread.start()
    logger.info("News digest generation started in the background.")