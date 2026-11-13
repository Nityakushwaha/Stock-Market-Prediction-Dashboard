from src.sentiment.analyzer import SentimentAnalyzer

print("Creating analyzer 1")
a1 = SentimentAnalyzer()

print("Creating analyzer 2")
a2 = SentimentAnalyzer()

print(a1.classifier is a2.classifier)
