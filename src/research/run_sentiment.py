from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.sentiment.analyzer import SentimentAnalyzer


INPUT = Path("data/processed/news_filtered.csv")
OUTPUT = Path("data/processed/news_sentiment.csv")

BATCH_SIZE = 32


def main() -> None:
    df = pd.read_csv(INPUT)

    print(f"Articles: {len(df):,}")
    print("Loading FinBERT...")

    analyzer = SentimentAnalyzer()

    results = []

    for start in range(0, len(df), BATCH_SIZE):
        end = min(start + BATCH_SIZE, len(df))

        batch = df.iloc[start:end]

        predictions = analyzer.analyze_batch(
            batch["headline"].tolist()
        )

        results.extend(predictions)

        print(
            f"Processed {end:,}/{len(df):,}",
            flush=True,
        )

    sentiment = pd.DataFrame(results)

    output_df = pd.concat(
        [
            df.reset_index(drop=True),
            sentiment,
        ],
        axis=1,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    output_df.to_csv(OUTPUT, index=False)

    print()
    print(f"Saved: {OUTPUT}")
    print(f"Rows: {len(output_df):,}")


if __name__ == "__main__":
    main()