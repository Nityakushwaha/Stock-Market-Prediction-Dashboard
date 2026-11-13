from __future__ import annotations

from src.models import Article


class NewsDeduplicator:
    """Remove duplicate news articles."""

    @staticmethod
    def deduplicate(articles: list[Article]) -> list[Article]:
        seen: set[str] = set()
        unique_articles: list[Article] = []

        for article in articles:
            key = article.title.strip().lower()

            if key in seen:
                continue

            seen.add(key)
            unique_articles.append(article)

        return unique_articles