from src.core.platform import NewsIntelligencePlatform

platform = NewsIntelligencePlatform()

result = platform.analyze("Tesla")

print(result["summary"]["kpis"])

print()

print(result["summary"]["charts"].keys())

print()

print(result["summary"]["tables"].keys())
