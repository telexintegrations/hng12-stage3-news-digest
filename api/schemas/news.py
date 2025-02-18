from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class Source(BaseModel):
    id: Optional[str] = None
    name: str

class NewsArticle(BaseModel):
    source: Source
    author: Optional[str] = None
    title: str
    description: Optional[str] = None
    url: HttpUrl
    urlToImage: Optional[HttpUrl] = None
    publishedAt: str
    content: Optional[str] = None

class NewsResponse(BaseModel):
    status: str
    totalResults: int
    articles: List[NewsArticle] 