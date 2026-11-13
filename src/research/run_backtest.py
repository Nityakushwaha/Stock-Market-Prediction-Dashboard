from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import pearsonr, spearmanr


INPUT = Path("data/processed/backtest_dataset.csv")
RETURNS = Path("data/processed/stock_returns.csv")

OUTPUT_DIR = Path("data/processed/backtest_results")


def add_momentum_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Add trailing 5-session return using only information available by anchor date."""

    prices = pd.read_csv(RETURNS)
    prices["date"] = pd.to_datetime(prices["date"])

    prices = prices.sort_values(["ticker", "date"])

    prices["momentum_5d"] = (
        prices.groupby("ticker")["close"].pct_change(5)
    )

    momentum = prices[
        ["ticker", "date", "momentum_5d"]
    ].rename(columns={"date": "anchor_date"})

    return df.merge(
        momentum,
        on=["ticker", "anchor_date"],
        how="left",
        validate="many_to_one",
    )


def correlation_stats(
    df: pd.DataFrame,
    sentiment_col: str,
    return_col: str,
) -> dict:

    clean = df[[sentiment_col, return_col]].dropna()

    if len(clean) < 3:
        return {
            "n": len(clean),
            "pearson_r": np.nan,
            "pearson_p": np.nan,
            "spearman_r": np.nan,
            "spearman_p": np.nan,
        }

    pearson = pearsonr(
        clean[sentiment_col],
        clean[return_col],
    )

    spearman = spearmanr(
        clean[sentiment_col],
        clean[return_col],
    )

    return {
        "n": len(clean),
        "pearson_r": pearson.statistic, # type: ignore
        "pearson_p": pearson.pvalue, # type: ignore
        "spearman_r": spearman.statistic, # type: ignore
        "spearman_p": spearman.pvalue, # type: ignore
    }


def regression_stats(
    df: pd.DataFrame,
    feature: str,
    target: str,
) -> dict:

    clean = df[
        [feature, target, "ticker"]
    ].dropna()

    if len(clean) < 10:
        return {
            "n": len(clean),
            "coefficient": np.nan,
            "t_stat": np.nan,
            "p_value": np.nan,
            "ci_low": np.nan,
            "ci_high": np.nan,
            "r_squared": np.nan,
        }

    X = sm.add_constant(clean[[feature]])
    y = clean[target]

    model = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={
            "groups": clean["ticker"],
        },
    )

    ci = model.conf_int().loc[feature]

    return {
        "n": len(clean),
        "coefficient": model.params[feature],
        "t_stat": model.tvalues[feature],
        "p_value": model.pvalues[feature],
        "ci_low": ci.iloc[0],
        "ci_high": ci.iloc[1],
        "r_squared": model.rsquared,
    }


def run_period(
    df: pd.DataFrame,
    period_name: str,
    start: str,
    end: str,
) -> pd.DataFrame:

    period = df[
        (df["date"] >= start)
        & (df["date"] <= end)
    ].copy()

    results = []

    for horizon in ["1d", "5d"]:

        target = f"forward_return_{horizon}"

        corr = correlation_stats(
            period,
            "sentiment_score",
            target,
        )

        reg = regression_stats(
            period,
            "sentiment_score",
            target,
        )

        results.append(
            {
                "period": period_name,
                "feature": "sentiment_score",
                "target": target,
                **corr,
                **{
                    f"reg_{k}": v
                    for k, v in reg.items()
                    if k != "n"
                },
            }
        )

        # Momentum-only baseline
        momentum_corr = correlation_stats(
            period,
            "momentum_5d",
            target,
        )

        momentum_reg = regression_stats(
            period,
            "momentum_5d",
            target,
        )

        results.append(
            {
                "period": period_name,
                "feature": "momentum_5d",
                "target": target,
                **momentum_corr,
                **{
                    f"reg_{k}": v
                    for k, v in momentum_reg.items()
                    if k != "n"
                },
            }
        )

    return pd.DataFrame(results)


def main() -> None:

    df = pd.read_csv(INPUT)

    # Multiple calendar news dates can map to the same trading
    # session (weekends/holidays). Collapse them to one observation
    # per stock/trading session to avoid reusing the same return.
    df["date"] = pd.to_datetime(df["date"])
    df["anchor_date"] = pd.to_datetime(df["anchor_date"])

    df["sentiment_weight"] = df["article_count"]

    grouped = (
        df.groupby(["ticker", "anchor_date"], as_index=False)
        .apply(
            lambda g: pd.Series(
                {
                    "date": g["date"].max(),
                    "sentiment_score": (
                        (g["sentiment_score"] * g["sentiment_weight"]).sum()
                        / g["sentiment_weight"].sum()
                    ),
                    "positive_probability": (
                        (g["positive_probability"] * g["sentiment_weight"]).sum()
                        / g["sentiment_weight"].sum()
                    ),
                    "neutral_probability": (
                        (g["neutral_probability"] * g["sentiment_weight"]).sum()
                        / g["sentiment_weight"].sum()
                    ),
                    "negative_probability": (
                        (g["negative_probability"] * g["sentiment_weight"]).sum()
                        / g["sentiment_weight"].sum()
                    ),
                    "article_count": g["article_count"].sum(),
                    "forward_return_1d": g["forward_return_1d"].iloc[0],
                    "forward_return_5d": g["forward_return_5d"].iloc[0],
                }
            ),
            include_groups=False, # type: ignore
        )
    ) # type: ignore

    df["date"] = pd.to_datetime(df["date"])
    df["anchor_date"] = pd.to_datetime(
        df["anchor_date"]
    )

    df = grouped.reset_index(drop=True)

    df = add_momentum_feature(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_DIR / "analysis_dataset.csv",
        index=False,
    )

    print(
        f"Analysis observations: {len(df):,}"
    )

    print(
        f"Stocks: {df['ticker'].nunique()}"
    )

    print("\nTrain: 2022")
    train = run_period(
        df,
        "train",
        "2022-01-01",
        "2022-12-31",
    )

    print("\nTest: 2023")
    test = run_period(
        df,
        "test",
        "2023-01-01",
        "2023-12-31",
    )

    results = pd.concat(
        [train, test],
        ignore_index=True,
    )

    results.to_csv(
        OUTPUT_DIR / "statistical_results.csv",
        index=False,
    )

    print("\n" + "=" * 100)
    print("STATISTICAL RESULTS")
    print("=" * 100)

    display_cols = [
        "period",
        "feature",
        "target",
        "n",
        "pearson_r",
        "pearson_p",
        "spearman_r",
        "spearman_p",
        "reg_coefficient",
        "reg_t_stat",
        "reg_p_value",
        "reg_ci_low",
        "reg_ci_high",
        "reg_r_squared",
    ]

    print(
        results[display_cols].round(6).to_string(
            index=False
        )
    )

    print(
        f"\nSaved: "
        f"{OUTPUT_DIR / 'statistical_results.csv'}"
    )


if __name__ == "__main__":
    main()