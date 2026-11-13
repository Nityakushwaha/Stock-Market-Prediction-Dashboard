from __future__ import annotations

from config.constants import MIN_RELEVANCE_SCORE
from src.analytics.news_summary import NewsSummary
from src.api.news_aggregator import NewsAggregator
from src.core.relevance_ranker import RelevanceRanker
from src.models import (
    Article,
    Company,
)
from src.sentiment.analyzer import SentimentAnalyzer


class NewsPipeline:
    """Complete news processing pipeline."""

    def __init__(self) -> None:
        self.aggregator = NewsAggregator()
        self.sentiment = SentimentAnalyzer()

    def _apply_sentiment(
        self,
        articles: list[Article],
    ) -> list[Article]:
        """Run FinBERT sentiment analysis."""

        for article in articles:
            result = self.sentiment.analyze_text(
                f"{article.title}\n\n{article.description}"
            )

            article.sentiment = result["sentiment"]
            article.sentiment_score = result["confidence"]

        return articles

    def process_company(
        self,
        company: Company,
    ) -> dict:
        """Process a known company."""

        articles = self.aggregator.fetch_company(company)

        articles = RelevanceRanker.rank(
            articles,
            company,
        )

        articles = self._apply_sentiment(articles)

        articles = [
            article
            for article in articles
            if article.relevance_score >= MIN_RELEVANCE_SCORE
        ]

        return {
            "articles": articles,
            "summary": NewsSummary.summarize(articles),
        }

    def process_query(
        self,
        query: str,
    ) -> dict:
        """Process a generic financial search."""

        articles = self.aggregator.fetch_query(query)

        articles = self._apply_sentiment(articles)

        return {
            "articles": articles,
            "summary": NewsSummary.summarize(articles),
        }