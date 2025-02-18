import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROJECT_NAME : str = "News Digest"
    PROJECT_VERSION : str = "1.0.0"
    PROJECT_DESCRIPTION: str = "The News Digest Bot is an automated news summarizer and broadcaster that fetches the latest news from a free news API (NewsAPI) and sends a digest of top headlines to a Telex channel every day."
    
    NEWS_API_KEY  : str = os.getenv("NEWS_API_KEY")
    NEWS_COUNTRY : str = os.getenv("NEWS_COUNTRY")
    TELEX_API_URL : str = os.getenv("TELEX_API_URL")
    SUMMARIZER_API_KEY : str = os.getenv("SUMMARIZER_API_KEY")