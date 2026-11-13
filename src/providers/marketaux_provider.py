from __future__ import annotations

from datetime import datetime

import requests

from config.settings import MARKETAUX_API_KEY
from src.models import (
    Article,
    Company,
)
from src.providers.base import BaseNewsProvider


class MarketauxProvider(BaseNewsProvider):
    """Marketaux provider."""

    BASE_URL = "https://api.marketaux.com/v1/news/all"

    def __init__(self) -> None:
        if not MARKETAUX_API_KEY:
            raise ValueError("MARKETAUX_API_KEY not configured.")

    @property
    def name(self) -> str:
        return "Marketaux"

    def _fetch(
        self,
        params: dict,
        company_name: str,
    ) -> list[Article]:
        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()

        articles: list[Article] = []

        for item in data.get("data", []):
            published_at = item.get("published_at")

            articles.append(
                Article(
                    provider=self.name,
                    company=company_name,
                    title=item.get("title", ""),
                    description=item.get("description", ""),
                    content=item.get("snippet", ""),
                    source=item.get("source", ""),
                    author=item.get("author"),
                    url=item.get("url", ""),
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
        params = {
            "api_token": MARKETAUX_API_KEY,
            "symbols": company.ticker.replace(".NS", ""),
            "filter_entities": "true",
            "language": "en",
            "published_after": "2026-07-01",
            "sort": "entity_match_score",
            "limit": limit,
        }

        return self._fetch(
            params=params,
            company_name=company.company,
        )

    def fetch_query(
        self,
        query: str,
        limit: int = 10,
    ) -> list[Article]:
        params = {
            "api_token": MARKETAUX_API_KEY,
            "search": query,
            "language": "en",
            "published_after": "2026-07-01",
            "limit": limit,
        }

        return self._fetch(
            params=params,
            company_name=query,
        )