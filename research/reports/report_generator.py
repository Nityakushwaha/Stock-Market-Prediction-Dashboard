from __future__ import annotations

from pathlib import Path

import pandas as pd

from research.benchmark.models import benchmark_result


class ReportGenerator:
    """Generates benchmark reports."""

    def save(
        self,
        results: list[benchmark_result.BenchmarkResult],
        output_path: str = "research/reports/benchmark_results.csv",
    ) -> None:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(
            [
                {
                    "provider": result.provider,
                    "company": result.company,
                    "total_articles": result.total_articles,
                    "average_age_hours": result.average_age_hours,
                    "response_time_ms": result.response_time_ms,
                }
                for result in results
            ]
        )

        df.to_csv(output_path, index=False)

        print(f"\nReport saved to: {output_path}")