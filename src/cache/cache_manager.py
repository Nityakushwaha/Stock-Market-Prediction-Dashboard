from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from config.constants import CACHE_TTL_MINUTES


class CacheManager:
    """
    Simple in-memory cache with TTL support.
    """

    def __init__(
        self,
        ttl_minutes: int = CACHE_TTL_MINUTES,
    ) -> None:
        self.ttl = timedelta(minutes=ttl_minutes)
        self._cache: dict[str, dict[str, Any]] = {}

    def get(self, key: str) -> Any | None:
        item = self._cache.get(key)

        if item is None:
            return None

        if datetime.now(UTC) > item["expires_at"]:
            del self._cache[key]
            return None

        return item["value"]

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = {
            "value": value,
            "expires_at": datetime.now(UTC) + self.ttl,
        }

    def clear(self) -> None:
        self._cache.clear()

    def contains(self, key: str) -> bool:
        return self.get(key) is not None
