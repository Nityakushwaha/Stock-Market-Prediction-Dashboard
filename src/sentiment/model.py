from __future__ import annotations

from functools import lru_cache
from typing import Any

from transformers import pipeline

MODEL_NAME = "ProsusAI/finbert"


@lru_cache(maxsize=1)
def get_classifier() -> Any:
    """
    Load and cache the FinBERT sentiment analysis pipeline.

    The model is loaded only once per Python process and reused
    for all subsequent sentiment analysis requests.
    """
    return pipeline(
        task="text-classification",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
        truncation=True,
    )
