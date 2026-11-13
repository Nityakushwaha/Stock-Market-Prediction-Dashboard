from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:
    """Canonical article model used by all providers."""
    
    provider: str
    company: str
    title: str
    description: str
    content: str
    source: str
    author: str | None
    url: str
    published_at: datetime | None

    relevance_score: int = 0

    sentiment: str = ""
    sentiment_score: float = 0.0