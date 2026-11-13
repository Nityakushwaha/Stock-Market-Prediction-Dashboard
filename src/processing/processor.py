from __future__ import annotations

import pandas as pd

from src.processing.cleaner import NewsCleaner
from src.sentiment.analyzer import SentimentAnalyzer


class NewsProcessor:
    """
    Enrich news articles with sentiment predictions.
    """

    def __init__(self) -> None:
        self.analyzer = SentimentAnalyzer()

    def process(self, news_df: pd.DataFrame) -> pd.DataFrame:
        """
        Return a new DataFrame enriched with sentiment.
        """

        if news_df.empty:
            return news_df.copy()

        processed = news_df.copy()

        texts = NewsCleaner.prepare_text(processed)

        predictions = self.analyzer.analyze_batch(texts.tolist())

        sentiments = [prediction["sentiment"] for prediction in predictions]

        confidences = [prediction["confidence"] for prediction in predictions]

        processed["sentiment"] = sentiments
        processed["confidence"] = confidences

        return processed
