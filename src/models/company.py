from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    """Represents a benchmark company."""

    ticker: str
    company: str
    country: str
    sector: str
    aliases: list[str]