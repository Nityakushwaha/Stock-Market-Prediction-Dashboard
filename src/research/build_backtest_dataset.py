from pathlib import Path

import numpy as np
import pandas as pd


SENTIMENT = Path("data/processed/daily_sentiment.csv")
RETURNS = Path("data/processed/stock_returns.csv")
OUTPUT = Path("data/processed/backtest_dataset.csv")


def align_sentiment_to_returns(
    sentiment: pd.DataFrame,
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """Map each sentiment date to the first trading session strictly after it."""

    results = []

    for ticker, group in sentiment.groupby("ticker"):
        price = returns[returns["ticker"] == ticker].sort_values("date")

        if price.empty:
            continue

        trading_dates = price["date"].to_numpy()

        group = group.sort_values("date").copy()

        positions = np.searchsorted(
            trading_dates,
            group["date"].to_numpy(),
            side="right",
        )

        valid = positions < len(price)

        group = group.loc[valid].copy()

        positions = positions[valid]

        price_rows = price.iloc[positions].copy()

        group["anchor_date"] = price_rows["date"].to_numpy()
        group["forward_return_1d"] = (
            price_rows["forward_return_1d"].to_numpy()
        )
        group["forward_return_5d"] = (
            price_rows["forward_return_5d"].to_numpy()
        )

        results.append(group)

    if not results:
        raise RuntimeError("No sentiment observations could be aligned.")

    return (
        pd.concat(results, ignore_index=True)
        .sort_values(["ticker", "date"])
        .reset_index(drop=True)
    )


def main() -> None:
    sentiment = pd.read_csv(SENTIMENT)
    returns = pd.read_csv(RETURNS)

    sentiment["date"] = pd.to_datetime(sentiment["date"])
    returns["date"] = pd.to_datetime(returns["date"])

    dataset = align_sentiment_to_returns(
        sentiment,
        returns,
    )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataset.to_csv(OUTPUT, index=False)

    print(f"Sentiment observations: {len(sentiment):,}")
    print(f"Aligned observations: {len(dataset):,}")
    print(f"Stocks: {dataset['ticker'].nunique()}")

    print("\nMissing forward returns:")
    print(
        dataset[
            [
                "forward_return_1d",
                "forward_return_5d",
            ]
        ].isna().sum()
    )

    print("\nSample alignment:")
    print(
        dataset[
            [
                "date",
                "ticker",
                "anchor_date",
                "sentiment_score",
                "forward_return_1d",
                "forward_return_5d",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )

    print(f"\nSaved: {OUTPUT}")


if __name__ == "__main__":
    main()