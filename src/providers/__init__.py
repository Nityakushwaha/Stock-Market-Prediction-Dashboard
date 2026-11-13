from src.providers.finnhub_provider import FinnhubProvider
from src.providers.marketaux_provider import MarketauxProvider
from src.providers.newsapi_provider import NewsAPIProvider


def get_providers():
    """Return all registered benchmark providers."""

    return [
        NewsAPIProvider(),
        MarketauxProvider(),
        FinnhubProvider(),
    ]