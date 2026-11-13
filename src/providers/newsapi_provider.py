from __future__ import annotations

from datetime import datetime

from newsapi import NewsApiClient

from config.settings import NEWS_API_KEY
from src.models import (
    Article,
    Company,
)
from src.providers.base import BaseNewsProvider


class NewsAPIProvider(BaseNewsProvider):
    """NewsAPI provider."""

    def __init__(self) -> None:
        if not NEWS_API_KEY:
            raise ValueError("NEWS_API_KEY not configured.")

        self.client = NewsApiClient(api_key=NEWS_API_KEY)

    @property
    def name(self) -> str:
        return "NewsAPI"

    def _fetch(
        self,
        query: str,
        company_name: str,
        limit: int,
    ) -> list[Article]:
        response = self.client.get_everything(
            q=query,
            language="en",
            sort_by="publishedAt",
            page_size=limit,
        )

        articles: list[Article] = []

        for item in response.get("articles", []):
            published_at = item.get("publishedAt")

            articles.append(
                Article(
                    provider=self.name,
                    company=company_name,
                    title=item.get("title") or "",
                    description=item.get("description") or "",
                    content=item.get("content") or "",
                    source=item.get("source", {}).get("name", ""),
                    author=item.get("author"),
                    url=item.get("url") or "",
                    published_at=(
                        datetime.fromisoformat(
                            published_at.replace("Z", "+00:00")
                        )
                        if published_at
                        else None
                    ),
                )
            )

        return articles

    def fetch_company(
        self,
        company: Company,
        limit: int = 10,
    ) -> list[Article]:
        return self._fetch(
            query=company.company,
            company_name=company.company,
            limit=limit,
        )

    def fetch_query(
        self,
        query: str,
        limit: int = 10,
    ) -> list[Article]:
        return self._fetch(
            query=query,
            company_name=query,
            limit=limit,
        )