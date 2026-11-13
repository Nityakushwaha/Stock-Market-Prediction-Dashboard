from __future__ import annotations

import pandas as pd

from src.analytics.aggregations import SentimentAggregations
from src.analytics.metrics import SentimentMetrics
from src.analytics.rankings import SentimentRankings


class AnalyticsService:
    """
    Generate dashboard-ready analytics.
    """

    def generate(self, df: pd.DataFrame) -> dict:
        sentiment_distribution = SentimentAggregations.sentiment_distribution(df)

        source_distribution = SentimentAggregations.source_distribution(df)

        daily_sentiment = SentimentAggregations.daily_sentiment(df)

        daily_article_count = SentimentAggregations.daily_article_count(df)

        kpis = {
            "overall_sentiment": SentimentMetrics.overall_sentiment(df),
            "average_confidence": SentimentMetrics.average_confidence(df),
            "article_count": SentimentMetrics.article_count(df),
        }

        charts = {
            "sentiment_distribution": sentiment_distribution,
            "source_distribution": source_distribution,
            "daily_sentiment": daily_sentiment,
            "daily_article_count": daily_article_count,
        }

        tables = {
            "most_positive": SentimentRankings.most_positive(df),
            "most_negative": SentimentRankings.most_negative(df),
            "latest_articles": df.sort_values(
                "published_at",
                ascending=False,
            ),
        }

        return {
            "kpis": kpis,
            "charts": charts,
            "tables": tables,
        }