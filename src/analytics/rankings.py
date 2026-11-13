from __future__ import annotations

import pandas as pd


class SentimentRankings:
    """
    Rank articles by confidence.
    """

    @staticmethod
    def most_positive(
        df: pd.DataFrame,
        limit: int = 5,
    ) -> pd.DataFrame:

        positive = df[df["sentiment"] == "Positive"]

        return positive.sort_values(
            "confidence",
            ascending=False,
        ).head(limit)

    @staticmethod
    def most_negative(
        df: pd.DataFrame,
        limit: int = 5,
    ) -> pd.DataFrame:

        negative = df[df["sentiment"] == "Negative"]

        return negative.sort_values(
            "confidence",
            ascending=False,
        ).head(limit)
