from __future__ import annotations

import pandas as pd


class SentimentAggregations:
    """
    Aggregate sentiment information.
    """

    @staticmethod
    def sentiment_distribution(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame(columns=["sentiment", "count"])

        return (
            df["sentiment"]
            .value_counts()
            .rename_axis("sentiment")
            .reset_index(name="count")
        )

    @staticmethod
    def source_distribution(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame(columns=["source", "count"])

        return (
            df["source"].value_counts().rename_axis("source").reset_index(name="count")
        )

    @staticmethod
    def daily_sentiment(df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate article counts by date and sentiment.
        """

        if df.empty:
            return pd.DataFrame(columns=["date", "sentiment", "count"])

        data = df.copy()

        data["published_at"] = pd.to_datetime(
            data["published_at"],
            errors="coerce",
            utc=True,
        )

        data = data.dropna(subset=["published_at"])

        data["date"] = data["published_at"].dt.date

        return (
            data.groupby(["date", "sentiment"])
            .size()
            .reset_index(name="count")
            .sort_values("date")
        )

    @staticmethod
    def daily_article_count(df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate article counts by date.
        """

        if df.empty:
            return pd.DataFrame(columns=["date", "count"])

        data = df.copy()

        data["published_at"] = pd.to_datetime(
            data["published_at"],
            errors="coerce",
            utc=True,
        )

        data = data.dropna(subset=["published_at"])

        data["date"] = data["published_at"].dt.date

        return data.groupby("date").size().reset_index(name="count").sort_values("date")
