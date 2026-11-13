from __future__ import annotations

from collections import Counter

from src.models import Article


class NewsSummary:
    """Generate summary statistics for a collection of articles."""

    @staticmethod
    def summarize(articles: list[Article]) -> dict:
        sentiments = Counter(article.sentiment for article in articles)
        providers = Counter(article.provider for article in articles)
        sources = Counter(article.source for article in articles)

        return {
            "total_articles": len(articles),
            "sentiments": dict(sentiments),
            "providers": dict(providers),
            "top_sources": dict(sources.most_common(10)),
            "average_relevance": (
                sum(article.relevance_score for article in articles) / len(articles)
                if articles
                else 0
            ),
            "average_sentiment_confidence": (
                sum(article.sentiment_score for article in articles) / len(articles)
                if articles
                else 0
            ),
        }