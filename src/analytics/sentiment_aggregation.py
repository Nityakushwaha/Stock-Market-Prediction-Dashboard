from __future__ import annotations

import pandas as pd


def aggregate_daily_sentiment(
    sentiment_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate article-level FinBERT probabilities into one
    daily sentiment observation per stock.

    Sentiment score:
        mean(positive_probability - negative_probability)

    Coverage is retained so we can later test whether article
    volume affects the strength of the signal.
    """

    required = {
        "date",
        "ticker",
        "positive_probability",
        "negative_probability",
        "neutral_probability",
    }

    missing = required - set(sentiment_df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    df = sentiment_df.copy()

    df["date"] = pd.to_datetime(df["date"])

    df["sentiment_score"] = (
        df["positive_probability"]
        - df["negative_probability"]
    )

    daily = (
        df.groupby(["ticker", "date"], as_index=False)
        .agg(
            sentiment_score=("sentiment_score", "mean"),
            positive_probability=(
                "positive_probability",
                "mean",
            ),
            neutral_probability=(
                "neutral_probability",
                "mean",
            ),
            negative_probability=(
                "negative_probability",
                "mean",
            ),
            article_count=("headline", "count"),
        )
    )

    daily["sentiment_direction"] = daily[
        "sentiment_score"
    ].apply(
        lambda x: (
            "positive"
            if x > 0
            else "negative"
            if x < 0
            else "neutral"
        )
    )

    return daily.sort_values(
        ["ticker", "date"]
    ).reset_index(drop=True)