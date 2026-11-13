from __future__ import annotations

from abc import ABC, abstractmethod

from src.models import (
    Article,
    Company,
)


class BaseNewsProvider(ABC):
    """Base interface for all news providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        ...

    @abstractmethod
    def fetch_company(
        self,
        company: Company,
        limit: int = 10,
    ) -> list[Article]:
        """Fetch news using a Company object."""
        ...

    @abstractmethod
    def fetch_query(
        self,
        query: str,
        limit: int = 10,
    ) -> list[Article]:
        """Fetch news using a free-text search query."""
        ...