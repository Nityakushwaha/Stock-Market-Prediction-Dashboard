from __future__ import annotations

import numpy as np
import pandas as pd


def add_12_month_growth_labels(
    prices: pd.DataFrame,
    *,
    max_target_gap_days: int = 7,
) -> pd.DataFrame:
    """Add a 12-month return and positive/negative label to adjusted prices.

    ``adjusted_close`` must account for stock splits and dividends. For each
    observation, the target price is the first available trading price on or
    after its 12-month anniversary. If that price is more than
    ``max_target_gap_days`` after the anniversary, the target is left missing
    rather than using a potentially incomplete price series.

    Returns above zero are labeled ``positive``; zero or below are labeled
    ``negative``. The final rows for each ticker have no label until future
    prices become available.
    """

    required = {"date", "ticker", "adjusted_close"}
    missing = required - set(prices.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if max_target_gap_days < 0:
        raise ValueError("max_target_gap_days must be zero or greater.")

    result = prices.copy().reset_index(drop=True)
    result["date"] = pd.to_datetime(result["date"], errors="coerce")
    result["adjusted_close"] = pd.to_numeric(
        result["adjusted_close"],
        errors="coerce",
    )

    if result[["date", "ticker", "adjusted_close"]].isna().any().any():
        raise ValueError("Prices contain missing or invalid required values.")

    if (result["adjusted_close"] <= 0).any():
        raise ValueError("adjusted_close values must be greater than zero.")

    if result.duplicated(["ticker", "date"]).any():
        raise ValueError("Each ticker must have at most one price per date.")

    result = result.sort_values(["ticker", "date"]).reset_index(drop=True)
    forward_returns = np.full(len(result), np.nan, dtype=float)
    labels = np.full(len(result), None, dtype=object)

    for _, positions in result.groupby("ticker", sort=False).indices.items():
        group = result.iloc[positions]
        dates = group["date"].to_numpy(dtype="datetime64[ns]")
        target_dates = (
            group["date"] + pd.DateOffset(months=12)
        ).to_numpy(dtype="datetime64[ns]")
        future_positions = np.searchsorted(dates, target_dates, side="left")
        has_future_price = future_positions < len(group)

        safe_positions = np.minimum(future_positions, len(group) - 1)
        actual_dates = dates[safe_positions]
        day_gaps = (actual_dates - target_dates).astype("timedelta64[D]").astype(int)
        valid = has_future_price & (day_gaps <= max_target_gap_days)

        if not valid.any():
            continue

        current_prices = group["adjusted_close"].to_numpy(dtype=float)
        returns = current_prices[future_positions[valid]] / current_prices[valid] - 1
        row_positions = positions[valid]

        forward_returns[row_positions] = returns
        labels[row_positions] = np.where(returns > 0, "positive", "negative")

    result["target_date"] = result["date"] + pd.DateOffset(months=12)
    result["forward_return_12m"] = forward_returns
    result["growth_label"] = pd.Series(labels, dtype="string")
    return result
