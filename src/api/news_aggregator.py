from __future__ import annotations

import logging

from src.core.deduplicator import NewsDeduplicator
from src.core.relevance_ranker import RelevanceRanker
from src.models import (
    Article,
    Company,
)
from src.providers import get_providers

logger = logging.getLogger(__name__)


class NewsAggregator:
    """Aggregate news from multiple providers."""

    def __init__(self) -> None:
        self.providers = get_providers()

    def fetch_company(
        self,
        company: Company,
    ) -> list[Article]:
        articles: list[Article] = []

        for provider in self.providers:
            try:
                articles.extend(provider.fetch_company(company))
            except Exception as error:
                logger.warning(
                    "%s provider failed: %s",
                    provider.name,
                    error,
                )

        articles = NewsDeduplicator.deduplicate(articles)
        articles = RelevanceRanker.rank(
            articles,
            company,
        )

        return articles

    def fetch_query(
        self,
        query: str,
    ) -> list[Article]:
        articles: list[Article] = []

        for provider in self.providers:
            try:
                articles.extend(provider.fetch_query(query))
            except Exception as error:
                logger.warning(
                    "%s provider failed: %s",
                    provider.name,
                    error,
                )

        articles = NewsDeduplicator.deduplicate(articles)

        return articles