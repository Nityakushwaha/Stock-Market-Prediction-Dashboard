from __future__ import annotations

from pathlib import Path

import pandas as pd

from config.universe import NIFTY_RESEARCH_UNIVERSE
from src.analytics.returns import calculate_forward_returns


PRICE_DIR = Path("data/raw/prices")
OUTPUT = Path("data/processed/stock_returns.csv")


def load_prices() -> pd.DataFrame:
    frames = []

    for ticker in NIFTY_RESEARCH_UNIVERSE:
        filename = "MM.csv" if ticker == "M&M" else f"{ticker}.csv"
        path = PRICE_DIR / filename

        if not path.exists():
            print(f"WARNING: missing {ticker}.csv")
            continue

        df = pd.read_csv(path)

        required = {"Date", "Close"}

        if not required.issubset(df.columns):
            raise ValueError(
                f"{path} missing required columns"
            )

        df = df[["Date", "Close"]].copy()

        df["date"] = pd.to_datetime(
            df["Date"],
            errors="coerce",
        )

        df["close"] = pd.to_numeric(
            df["Close"],
            errors="coerce",
        )

        df = df[
            (df["date"] >= "2022-01-01")
            & (df["close"] > 0)
        ]

        df["ticker"] = ticker

        df = df.dropna(
            subset=["date", "close"]
        )

        frames.append(
            df[
                ["date", "ticker", "close"]
            ]
        )

    if not frames:
        raise RuntimeError("No price data loaded.")

    return pd.concat(
        frames,
        ignore_index=True,
    )


def main() -> None:
    prices = load_prices()

    print(
        f"Loaded price observations: {len(prices):,}"
    )

    print(
        f"Stocks: {prices['ticker'].nunique()}"
    )

    returns = calculate_forward_returns(prices)

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    returns.to_csv(
        OUTPUT,
        index=False,
    )

    print(f"Saved: {OUTPUT}")
    print(
        f"Date range: "
        f"{returns['date'].min().date()} → "
        f"{returns['date'].max().date()}"
    )

    print("\nMissing forward returns:")
    print(
        returns[
            [
                "forward_return_1d",
                "forward_return_5d",
            ]
        ].isna().sum()
    )

    print("\nSample:")
    print(
        returns.head(10).to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()