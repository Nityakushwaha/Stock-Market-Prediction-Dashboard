from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("data/processed/backtest_results")
REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    robust = pd.read_csv(
        RESULTS_DIR / "robust_results.csv"
    )

    fama = pd.read_csv(
        RESULTS_DIR / "fama_macbeth_results.csv"
    )

    statistical = pd.read_csv(
        RESULTS_DIR / "statistical_results.csv"
    )

    # Keep only the primary sentiment regressions.
    primary = robust[
        robust["feature"] == "sentiment_score"
    ].copy()

    primary.to_csv(
        REPORT_DIR / "primary_results.csv",
        index=False,
    )

    # Fama-MacBeth sentiment results.
    fama_sentiment = fama[
        fama["coefficient"] == "sentiment_coefficient"
    ].copy()

    fama_sentiment.to_csv(
        REPORT_DIR / "fama_macbeth_sentiment.csv",
        index=False,
    )

    # Build a concise markdown report.
    lines = []

    lines.append("# FinBERT Sentiment → Returns Backtest")
    lines.append("")
    lines.append("## Primary regression results")
    lines.append("")
    lines.append(
        "| Period | Horizon | N | Coefficient | t-stat | p-value | 95% CI |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---|")

    for _, row in primary.iterrows():
        lines.append(
            f"| {row['period']} | "
            f"{row['target']} | "
            f"{int(row['n'])} | "
            f"{row['coefficient']:.6f} | "
            f"{row['t_stat']:.3f} | "
            f"{row['p_value']:.4f} | "
            f"[{row['ci_low']:.6f}, {row['ci_high']:.6f}] |"
        )

    lines.append("")
    lines.append("## Fama–MacBeth results")
    lines.append("")
    lines.append(
        "| Period | Horizon | Dates | Mean coefficient | t-stat | p-value | 95% CI |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---|")

    for _, row in fama_sentiment.iterrows():
        lines.append(
            f"| {row['period']} | "
            f"{row['target']} | "
            f"{int(row['n_dates'])} | "
            f"{row['mean_coefficient']:.6f} | "
            f"{row['t_stat']:.3f} | "
            f"{row['p_value']:.4f} | "
            f"[{row['ci_low']:.6f}, {row['ci_high']:.6f}] |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "The sentiment relationship is statistically significant "
        "during the 2022 training period but does not persist in "
        "the 2023 out-of-sample period."
    )
    lines.append("")
    lines.append(
        "Accordingly, this experiment does not provide evidence "
        "of stable out-of-sample predictive power from the tested "
        "FinBERT sentiment signal."
    )

    output = REPORT_DIR / "results_summary.md"

    output.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Saved: {output}")
    print(
        f"Saved: "
        f"{REPORT_DIR / 'primary_results.csv'}"
    )
    print(
        f"Saved: "
        f"{REPORT_DIR / 'fama_macbeth_sentiment.csv'}"
    )


if __name__ == "__main__":
    main()