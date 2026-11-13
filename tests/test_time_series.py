from src.core.platform import NewsIntelligencePlatform

platform = NewsIntelligencePlatform()

result = platform.analyze("Tesla")

print(result["summary"]["charts"]["daily_sentiment"])

print()

print(result["summary"]["charts"]["daily_article_count"])
