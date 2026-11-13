from __future__ import annotations

from src.analytics.service import AnalyticsService
from src.api.news_service import NewsService
from src.cache.cache_manager import CacheManager
from src.processing.processor import NewsProcessor


class NewsIntelligencePlatform:
    """Orchestrates the complete news analysis workflow."""

    def __init__(self) -> None:
        self.news_service = NewsService()
        self.processor = NewsProcessor()
        self.analytics = AnalyticsService()
        self.cache = CacheManager()

    def analyze(self, company: str) -> dict:
        cache_key = company.strip().lower()

        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        news = self.news_service.fetch_news(company)

        if news.empty:
            raise ValueError(f"No recent news found for '{company}'.")

        processed = self.processor.process(news)

        summary = self.analytics.generate(processed)

        result = {
            "company": company,
            "news": processed,
            "summary": summary,
        }

        self.cache.set(cache_key, result)

        return result

    def analyze_many(self, companies: list[str]) -> dict:
        companies = list(dict.fromkeys(companies))

        results = [self.analyze(company) for company in companies]

        comparison = []

        for result in results:
            kpis = result["summary"]["kpis"]

            comparison.append(
                {
                    "company": result["company"],
                    "overall_sentiment": kpis["overall_sentiment"],
                    "article_count": kpis["article_count"],
                    "average_confidence": kpis["average_confidence"],
                }
            )

        return {
            "companies": results,
            "comparison": comparison,
        }
