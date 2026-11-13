from __future__ import annotations

from src.sentiment.model import get_classifier


class SentimentAnalyzer:
    """Performs financial sentiment inference using FinBERT."""

    def __init__(self) -> None:
        self.classifier = get_classifier()

    def analyze_batch(self, texts: list[str]) -> list[dict]:
        """Return FinBERT probabilities and the most likely sentiment."""

        if not texts:
            return []

        cleaned = [text if text else "" for text in texts]
        predictions = self.classifier(cleaned, top_k=None)
        results = []

        for prediction in predictions:
            probabilities = {
                item["label"].lower(): float(item["score"])
                for item in prediction
            }

            sentiment = max(
                ("positive", "neutral", "negative"),
                key=lambda label: probabilities.get(label, 0.0),
            )

            results.append(
                {
                    "positive_probability": probabilities.get("positive", 0.0),
                    "neutral_probability": probabilities.get("neutral", 0.0),
                    "negative_probability": probabilities.get("negative", 0.0),
                    # Keep one display format across the dashboard so its
                    # charts, badges, rankings, and KPI filters agree.
                    "sentiment": sentiment.title(),
                    "confidence": probabilities.get(sentiment, 0.0),
                }
            )

        return results

    def analyze_text(self, text: str) -> dict:
        """Analyze one article or text passage."""
        return self.analyze_batch([text])[0]
