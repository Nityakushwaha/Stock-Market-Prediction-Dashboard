from __future__ import annotations

from datetime import datetime, timezone

from research.benchmark.models import BenchmarkResult
from src.models import (
    Article,
    Company,
)


class BenchmarkEvaluator:
    """Evaluates benchmark metrics for news providers."""

    def _classify_articles(
        self,
        company: Company,
        articles: list[Article],
    ) -> tuple[int, int, int]:
        """Classify articles as primary, secondary, or irrelevant."""

        aliases = [company.company.lower(), company.ticker.lower()]
        aliases.extend(alias.lower() for alias in company.aliases)

        primary = 0
        secondary = 0
        irrelevant = 0

        for article in articles:
            title = article.title.lower()
            description = article.description.lower()

            title_score = 0
            description_score = 0

            for alias in aliases:
                if alias in title:
                    title_score += 1
                if alias in description:
                    description_score += 1

            if title_score > 0:
                primary += 1
            elif description_score > 0:
                secondary += 1
            else:
                irrelevant += 1

        return primary, secondary, irrelevant

    def evaluate(
        self,
        provider: str,
        company: Company,
        articles: list[Article],
        response_time_ms: float = 0.0,
    ) -> BenchmarkResult:
        """Evaluate a provider's benchmark performance."""

        now = datetime.now(timezone.utc)

        ages = [
            (now - article.published_at).total_seconds() / 3600
            for article in articles
            if article.published_at
        ]

        average_age = sum(ages) / len(ages) if ages else 0.0

        titles = [article.title.strip().lower() for article in articles]
        duplicate_articles = len(titles) - len(set(titles))

        primary, secondary, irrelevant = self._classify_articles(
            company,
            articles,
        )

        return BenchmarkResult(
            provider=provider,
            company=company.company,
            total_articles=len(articles),
            primary_articles=primary,
            secondary_articles=secondary,
            irrelevant_articles=irrelevant,
            duplicate_articles=duplicate_articles,
            average_age_hours=average_age,
            response_time_ms=response_time_ms,
        )