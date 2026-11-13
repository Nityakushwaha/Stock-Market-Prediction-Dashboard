from __future__ import annotations

import pandas as pd


def calculate_forward_returns(
    prices: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate forward close-to-close returns.

    t+1:
        Close(t+1) / Close(t) - 1

    t+5:
        Close(t+5) / Close(t) - 1

    The shift(-N) is intentional: these are FUTURE returns
    relative to the sentiment date.
    """

    required = {"date", "ticker", "close"}

    missing = required - set(prices.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    df = prices.copy()

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(["ticker", "date"])

    grouped = df.groupby("ticker")["close"]

    df["forward_return_1d"] = (
        grouped.shift(-1) / df["close"] - 1
    )

    df["forward_return_5d"] = (
        grouped.shift(-5) / df["close"] - 1
    )

    return df.reset_index(drop=True)