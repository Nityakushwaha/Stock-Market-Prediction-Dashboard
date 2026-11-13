from pathlib import Path

from src.data.news_filter import (
    filter_news,
    load_economic_times,
)


DATA_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "news"
    / "economic_times"
)


def main() -> None:
    print("Loading Economic Times data...")

    news = load_economic_times(DATA_DIR)

    print(f"Raw articles: {len(news):,}")

    filtered = filter_news(news)

    print(f"Stock-linked observations: {len(filtered):,}")

    print("\nArticles by ticker:")
    print(
        filtered["ticker"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nArticles by year:")
    print(
        filtered.groupby(filtered["date"].dt.year)
        .size()
        .to_string()
    )

    print("\nUnique URLs:")
    print(filtered["url"].nunique())

    print("\nUnique headlines:")
    print(filtered["headline"].nunique())

    print("\nSample matches:")
    print(
        filtered[
            [
                "date",
                "ticker",
                "headline",
                "matched_alias",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
