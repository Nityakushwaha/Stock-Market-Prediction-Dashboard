from time import perf_counter

from src.core.platform import NewsIntelligencePlatform

platform = NewsIntelligencePlatform()

start = perf_counter()
platform.analyze("Tesla")
print(f"First call : {perf_counter() - start:.2f}s")

start = perf_counter()
platform.analyze("Tesla")
print(f"Second call: {perf_counter() - start:.2f}s")
