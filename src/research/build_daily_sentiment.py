from pathlib import Path

import pandas as pd

from src.analytics.sentiment_aggregation import (
    aggregate_daily_sentiment,
)


INPUT = Path("data/processed/news_sentiment.csv")
OUTPUT = Path("data/processed/daily_sentiment.csv")


def main() -> None:
    df = pd.read_csv(INPUT)

    daily = aggregate_daily_sentiment(df)

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    daily.to_csv(OUTPUT, index=False)

    print(f"Article observations: {len(df):,}")
    print(f"Daily stock observations: {len(daily):,}")
    print(f"Stocks: {daily['ticker'].nunique()}")
    print(f"Date range: {daily['date'].min()} → {daily['date'].max()}")
    print(f"Saved: {OUTPUT}")

    print("\nArticle-count summary:")
    print(daily["article_count"].describe())

    print("\nSample:")
    print(daily.head(10).to_string(index=False))


if __name__ == "__main__":
    main()