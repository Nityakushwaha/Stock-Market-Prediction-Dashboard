from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import pearsonr, spearmanr


INPUT = Path("data/processed/backtest_results/analysis_dataset.csv")
OUTPUT = Path(
    "data/processed/backtest_results/robust_results.csv"
)


def run_regression(
    df: pd.DataFrame,
    feature: str,
    target: str,
) -> dict:

    clean = df[[feature, target]].dropna()

    X = sm.add_constant(clean[[feature]])
    y = clean[target]

    # HAC/Newey-West standard errors account for
    # serial dependence in the observations.
    model = sm.OLS(y, X).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": 5},
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
    name: str,
    start: str,
    end: str,
) -> list[dict]:

    period = df[
        (df["anchor_date"] >= start)
        & (df["anchor_date"] <= end)
    ].copy()

    results = []

    for horizon in ["1d", "5d"]:

        target = f"forward_return_{horizon}"

        stats = run_regression(
            period,
            "sentiment_score",
            target,
        )

        results.append(
            {
                "period": name,
                "feature": "sentiment_score",
                "target": target,
                **stats,
            }
        )

        # Sentiment + momentum control
        clean = period[
            [
                "sentiment_score",
                "momentum_5d",
                target,
            ]
        ].dropna()

        X = sm.add_constant(
            clean[
                [
                    "sentiment_score",
                    "momentum_5d",
                ]
            ]
        )

        model = sm.OLS(
            clean[target],
            X,
        ).fit(
            cov_type="HAC",
            cov_kwds={"maxlags": 5},
        )

        ci = model.conf_int().loc[
            "sentiment_score"
        ]

        results.append(
            {
                "period": name,
                "feature": "sentiment_plus_momentum",
                "target": target,
                "n": len(clean),
                "coefficient": model.params[
                    "sentiment_score"
                ],
                "t_stat": model.tvalues[
                    "sentiment_score"
                ],
                "p_value": model.pvalues[
                    "sentiment_score"
                ],
                "ci_low": ci.iloc[0],
                "ci_high": ci.iloc[1],
                "r_squared": model.rsquared,
            }
        )

    return results


def main():

    df = pd.read_csv(INPUT)

    df["date"] = pd.to_datetime(df["date"])
    df["anchor_date"] = pd.to_datetime(
        df["anchor_date"]
    )

    results = []

    results.extend(
        run_period(
            df,
            "train_2022",
            "2022-01-01",
            "2022-12-31",
        )
    )

    results.extend(
        run_period(
            df,
            "test_2023",
            "2023-01-01",
            "2023-12-31",
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