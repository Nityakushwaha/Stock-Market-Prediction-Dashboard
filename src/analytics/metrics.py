from __future__ import annotations

import pandas as pd


class SentimentMetrics:
    """
    Compute high-level sentiment metrics.
    """

    @staticmethod
    def overall_sentiment(df: pd.DataFrame) -> str:
        if df.empty:
            return "No Data"

        return df["sentiment"].mode().iloc[0]

    @staticmethod
    def average_confidence(df: pd.DataFrame) -> float:
        if df.empty:
            return 0.0

        return float(round(df["confidence"].mean(), 3))

    @staticmethod
    def article_count(df: pd.DataFrame) -> int:
        return len(df)
