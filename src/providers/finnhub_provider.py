from __future__ import annotations

from datetime import datetime, timedelta, timezone

import requests

from config.settings import FINNHUB_API_KEY
from src.models import (
    Article,
    Company,
)
from src.providers.base import BaseNewsProvider


class FinnhubProvider(BaseNewsProvider):
    """Finnhub provider."""

    COMPANY_URL = "https://finnhub.io/api/v1/company-news"
    GENERAL_URL = "https://finnhub.io/api/v1/news"

    def __init__(self) -> None:
        if not FINNHUB_API_KEY:
            raise ValueError("FINNHUB_API_KEY not configured.")

    @property
    def name(self) -> str:
        return "Finnhub"

    def _build_articles(
        self,
        data: list[dict],
        company_name: str,
        limit: int,
    ) -> list[Article]:
        articles: list[Article] = []

        for item in data[:limit]:
            articles.append(
                Article(
                    provider=self.name,
                    company=company_name,
                    title=item.get("headline", ""),
                    description=item.get("summary", ""),
                    content="",
                    source=item.get("source", ""),
                    author=None,
                    url=item.get("url", ""),
                    published_at=(
                        datetime.fromtimestamp(
                            item["datetime"],
                            tz=timezone.utc,
                        )
                        if item.get("datetime")
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
        today = datetime.now(timezone.utc).date()
        start = today - timedelta(days=30)

        params = {
            "symbol": company.ticker.replace(".NS", ""),
            "from": start.isoformat(),
            "to": today.isoformat(),
            "token": FINNHUB_API_KEY,
        }

        response = requests.get(
            self.COMPANY_URL,
            params=params,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()

        return self._build_articles(
            data=data,
            company_name=company.company,
            limit=limit,
        )

    def fetch_query(
        self,
        query: str,
        limit: int = 10,
    ) -> list[Article]:
        # Finnhub free tier doesn't support arbitrary keyword search.
        # Use general market news as a fallback for now.
        params = {
            "category": "general",
            "token": FINNHUB_API_KEY,
        }

        response = requests.get(
            self.GENERAL_URL,
            params=params,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()

        filtered = [
            article
            for article in data
            if query.lower() in (
                f"{article.get('headline', '')} "
                f"{article.get('summary', '')}"
            ).lower()
        ]

        return self._build_articles(
            data=filtered,
            company_name=query,
            limit=limit,
        )