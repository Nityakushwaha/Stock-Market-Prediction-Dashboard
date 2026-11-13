from __future__ import annotations

import pandas as pd

from research.benchmark.dataset_loader import load_companies
from src.core.news_pipeline import NewsPipeline
from src.validation.validator import NewsValidator


class NewsService:
    """Fetch and process financial news."""

    def __init__(self) -> None:
        self.pipeline = NewsPipeline()
        self.companies = load_companies(
            "research/datasets/companies.csv"
        )

    def _resolve_query(self, query: str):
        """
        Return a Company if the query matches one,
        otherwise return the raw query string.
        """

        query = query.strip().lower()

        for company in self.companies:

            if query == company.company.lower():
                return company

            if query == company.ticker.lower():
                return company

            if query in [alias.lower() for alias in company.aliases]:
                return company

        return query

    def fetch_news(
        self,
        query: str,
    ) -> pd.DataFrame:

        query = NewsValidator.validate_query(query)

        resolved = self._resolve_query(query)

        if isinstance(resolved, str):
            result = self.pipeline.process_query(resolved)
        else:
            result = self.pipeline.process_company(resolved)

        articles = result["articles"]

        if not articles:
            return pd.DataFrame()

        rows = []

        for article in articles:
            rows.append(
                {
                    "company": article.company,
                    "provider": article.provider,
                    "source": article.source,
                    "author": article.author,
                    "title": article.title,
                    "description": article.description,
                    "content": article.content,
                    "url": article.url,
                    "published_at": (
                        article.published_at.isoformat()
                        if article.published_at
                        else None
                    ),
                    "sentiment": article.sentiment,
                    "confidence": article.sentiment_score,
                    "relevance": article.relevance_score,
                }
            )

        return pd.DataFrame(rows)