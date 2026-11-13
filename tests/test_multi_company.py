from src.core.platform import NewsIntelligencePlatform

platform = NewsIntelligencePlatform()

result = platform.analyze_many(
    [
        "Tesla",
        "Apple",
        "Microsoft",
        "Tesla",
    ]
)

for company in result["comparison"]:
    print(company)
