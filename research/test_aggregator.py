from research.benchmark.dataset_loader import load_companies
from src.core.news_pipeline import NewsPipeline


def main() -> None:
    company = load_companies(
        "research/datasets/companies.csv"
    )[2]  # NVIDIA

    pipeline = NewsPipeline()

    result = pipeline.process(company) # type: ignore

    articles = result["articles"] # type: ignore
    summary = result["summary"] # type: ignore

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(summary)
    print()

    print("=" * 70)
    print(f"Fetched {len(articles)} articles.")
    print("=" * 70)
    print()

    for article in articles[:10]:
        print(
            f"[{article.relevance_score}] "
            f"{article.sentiment} "
            f"({article.sentiment_score:.2f})"
        )
        print(article.title)
        print(f"Source   : {article.source}")
        print(f"Provider : {article.provider}")
        print()


if __name__ == "__main__":
    main()