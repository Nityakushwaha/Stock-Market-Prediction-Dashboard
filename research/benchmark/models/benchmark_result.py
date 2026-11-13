from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    provider: str
    company: str

    total_articles: int

    primary_articles: int
    secondary_articles: int
    irrelevant_articles: int

    duplicate_articles: int

    average_age_hours: float

    response_time_ms: float