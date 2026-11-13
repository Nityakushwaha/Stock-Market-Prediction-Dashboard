from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT = Path("data/processed/backtest_results/analysis_dataset.csv")
OUTPUT = Path("research/figures")
OUTPUT.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(INPUT)
    df["anchor_date"] = pd.to_datetime(df["anchor_date"])

    # ---------------------------------------------------------
    # 1. Sentiment vs next-day return
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 6))

    train = df[df["anchor_date"].dt.year == 2022]
    test = df[df["anchor_date"].dt.year == 2023]

    ax.scatter(
        train["sentiment_score"],
        train["forward_return_1d"],
        alpha=0.25,
        s=12,
        label="2022 Train",
    )

    ax.scatter(
        test["sentiment_score"],
        test["forward_return_1d"],
        alpha=0.25,
        s=12,
        label="2023 Test",
    )

    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)

    ax.set_xlabel("Daily FinBERT Sentiment Score")
    ax.set_ylabel("Next-Trading-Day Return")
    ax.set_title("FinBERT Sentiment vs Next-Day Return")
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        OUTPUT / "sentiment_vs_next_day_return.png",
        dpi=200,
    )
    plt.close(fig)

    # ---------------------------------------------------------
    # 2. Average return by sentiment quintile
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 6))

    df["sentiment_quintile"] = pd.qcut(
        df["sentiment_score"],
        5,
        labels=[
            "Q1\nMost Negative",
            "Q2",
            "Q3",
            "Q4",
            "Q5\nMost Positive",
        ],
        duplicates="drop",
    )

    quintile = (
        df.groupby(
            ["anchor_date", "sentiment_quintile"],
            observed=True,
        )["forward_return_1d"]
        .mean()
        .reset_index()
    )

    quintile_avg = (
        quintile.groupby(
            "sentiment_quintile",
            observed=True,
        )["forward_return_1d"]
        .mean()
    )

    quintile_avg.plot(
        kind="bar",
        ax=ax,
    )

    ax.axhline(0, linewidth=0.8)

    ax.set_xlabel("Sentiment Quintile")
    ax.set_ylabel("Average Next-Trading-Day Return")
    ax.set_title(
        "Next-Day Return by FinBERT Sentiment Quintile"
    )

    fig.tight_layout()
    fig.savefig(
        OUTPUT / "return_by_sentiment_quintile.png",
        dpi=200,
    )
    plt.close(fig)

    # ---------------------------------------------------------
    # 3. Article coverage
    # ---------------------------------------------------------
    coverage = (
        df.groupby("ticker")
        .agg(
            observations=("ticker", "size"),
            total_articles=("article_count", "sum"),
        )
        .sort_values("observations")
    )

    fig, ax = plt.subplots(figsize=(11, 7))

    coverage["observations"].plot(
        kind="barh",
        ax=ax,
    )

    ax.set_xlabel("News-Return Observations")
    ax.set_ylabel("Ticker")
    ax.set_title(
        "News Coverage Across Research Universe"
    )

    fig.tight_layout()
    fig.savefig(
        OUTPUT / "news_coverage_by_stock.png",
        dpi=200,
    )
    plt.close(fig)

    print(f"Saved plots to: {OUTPUT}")


if __name__ == "__main__":
    main()