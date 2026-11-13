from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import ClassVar

from src.models import Article, Company


class RelevanceRanker:
    """Rank articles by weighted relevance."""


    FINANCIAL_KEYWORDS: ClassVar[set[str]] = {
        "earnings",
        "revenue",
        "profit",
        "guidance",
        "forecast",
        "stock",
        "shares",
        "market",
        "investor",
        "investment",
        "analyst",
        "rating",
        "price target",
        "acquisition",
        "merger",
        "ai",
        "chip",
        "semiconductor",
        "gpu",
    }

    TRUSTED_SOURCES: ClassVar[set[str]] = {
        "Reuters",
        "Bloomberg",
        "CNBC",
        "Yahoo",
        "MarketWatch",
        "Financial Times",
        "Seeking Alpha",
        "The Times of India",
    }

    COMPETITORS: ClassVar[set[str]] = {
        "amd",
        "intel",
        "qualcomm",
        "broadcom",
        "tsmc",
        "micron",
        "arm",
    }

    @classmethod
    def rank(
        cls,
        articles: list[Article],
        company: Company,
    ) -> list[Article]:

        aliases = {
            company.company.lower(),
            company.ticker.lower(),
            *[alias.lower() for alias in company.aliases],
        }

        now = datetime.now(timezone.utc)

        for article in articles:
            score = 0

            title = article.title.lower()
            description = article.description.lower()

            # Company mentions
            for alias in aliases:
                if alias in title:
                    score += 10

                if alias in description:
                    score += 4

            # Financial keywords
            for keyword in cls.FINANCIAL_KEYWORDS:
                if keyword in title:
                    score += 3
                elif keyword in description:
                    score += 1

            # Trusted source
            if article.source in cls.TRUSTED_SOURCES:
                score += 2

            # Freshness
            if article.published_at:
                age = now - article.published_at

                if age <= timedelta(hours=24):
                    score += 2
                elif age <= timedelta(days=3):
                    score += 1

            # Competitor penalty
            if not any(alias in title for alias in aliases):
                for competitor in cls.COMPETITORS:
                    if competitor in title:
                        score -= 8

            article.relevance_score = max(score, 0)

        return sorted(
            articles,
            key=lambda article: article.relevance_score,
            reverse=True,
        )