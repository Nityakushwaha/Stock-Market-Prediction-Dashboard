from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


INPUT = Path(
    "data/processed/backtest_results/analysis_dataset.csv"
)

OUTPUT = Path(
    "data/processed/backtest_results/fama_macbeth_results.csv"
)


def cross_sectional_coefficients(
    df: pd.DataFrame,
    target: str,
) -> pd.DataFrame:

    coefficients = []

    for date, group in df.groupby("anchor_date"):

        clean = group[
            ["sentiment_score", "momentum_5d", target]
        ].dropna()

        if len(clean) < 5:
            continue

        X = sm.add_constant(
            clean[
                ["sentiment_score", "momentum_5d"]
            ]
        )

        model = sm.OLS(
            clean[target],
            X,
        ).fit()

        coefficients.append(
            {
                "date": date,
                "sentiment_coefficient":
                    model.params["sentiment_score"],
                "momentum_coefficient":
                    model.params["momentum_5d"],
            }
        )

    return pd.DataFrame(coefficients)


def summarize(
    coefficients: pd.DataFrame,
    coefficient: str,
    period: str,
    target: str,
) -> dict:

    values = coefficients[coefficient].dropna()

    n = len(values)

    if n < 2:
        return {
            "period": period,
            "target": target,
            "coefficient": coefficient,
            "n_dates": n,
            "mean_coefficient": np.nan,
            "t_stat": np.nan,
            "p_value": np.nan,
            "ci_low": np.nan,
            "ci_high": np.nan,
        }

    mean = values.mean()
    se = values.std(ddof=1) / np.sqrt(n)

    t_stat = mean / se

    # Normal approximation is adequate for large n.
    p_value = 2 * (1 - __import__("scipy").stats.norm.cdf(abs(t_stat)))

    return {
        "period": period,
        "target": target,
        "coefficient": coefficient,
        "n_dates": n,
        "mean_coefficient": mean,
        "t_stat": t_stat,
        "p_value": p_value,
        "ci_low": mean - 1.96 * se,
        "ci_high": mean + 1.96 * se,
    }


def main():

    df = pd.read_csv(INPUT)

    df["anchor_date"] = pd.to_datetime(
        df["anchor_date"]
    )

    results = []

    periods = [
        ("train_2022", "2022-01-01", "2022-12-31"),
        ("test_2023", "2023-01-01", "2023-12-31"),
    ]

    for period, start, end in periods:

        subset = df[
            (df["anchor_date"] >= start)
            & (df["anchor_date"] <= end)
        ]

        for horizon in ["1d", "5d"]:

            target = f"forward_return_{horizon}"

            coefficients = cross_sectional_coefficients(
                subset,
                target,
            )

            for feature in [
                "sentiment_coefficient",
                "momentum_coefficient",
            ]:

                results.append(
                    summarize(
                        coefficients,
                        feature,
                        period,
                        target,
                    )
                )

    results = pd.DataFrame(results)

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results.to_csv(
        OUTPUT,
        index=False,
    )

    print(
        results.round(6).to_string(index=False)
    )

    print(f"\nSaved: {OUTPUT}")


if __name__ == "__main__":
    main()