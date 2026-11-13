from __future__ import annotations

import time

from research.benchmark.dataset_loader import load_companies
from research.benchmark.evaluator import BenchmarkEvaluator
from research.reports.report_generator import ReportGenerator
from src.providers import get_providers


def main() -> None:
    companies = load_companies("research/datasets/companies.csv")

    # Limit companies while developing
    companies = companies[:3]

    providers = get_providers()

    print("\nRegistered providers:")
    for provider in providers:
        print(f" - {provider.name}")

    evaluator = BenchmarkEvaluator()
    benchmark_results = []

    for company in companies:
        print("\n" + "=" * 80)
        print(f"Benchmarking: {company.company} ({company.ticker})")
        print("=" * 80)

        for provider in providers:
            print("\n" + "-" * 70)
            print(f"Provider: {provider.name}")
            print("-" * 70)

            try:
                print(f"Calling {provider.name}...")

                start = time.perf_counter()
                articles = provider.fetch(company)
                end = time.perf_counter()

                response_time_ms = (end - start) * 1000

                result = evaluator.evaluate(
                    provider=provider.name,
                    company=company,
                    articles=articles,
                    response_time_ms=response_time_ms,
                )

                benchmark_results.append(result)

                print(f"Articles             : {result.total_articles}")
                print(f"Primary              : {result.primary_articles}")
                print(f"Secondary            : {result.secondary_articles}")
                print(f"Irrelevant           : {result.irrelevant_articles}")
                print(f"Duplicates           : {result.duplicate_articles}")
                print(f"Average Age (hours)  : {result.average_age_hours:.2f}")
                print(f"Response Time (ms)   : {result.response_time_ms:.2f}")

            except Exception as error:
                print(f"❌ {provider.name} failed")
                print(type(error).__name__)
                print(error)

    ReportGenerator().save(benchmark_results)

    print("\nBenchmark completed successfully.")


if __name__ == "__main__":
    main()