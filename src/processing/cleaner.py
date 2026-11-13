from __future__ import annotations

import pandas as pd


class NewsCleaner:
    """
    Clean and prepare news articles for sentiment analysis.
    """

    @staticmethod
    def prepare_text(df: pd.DataFrame) -> pd.Series:
        """
        Build the text that will be sent to FinBERT.

        Preference:
        1. title + description
        2. title only
        3. description only
        """

        title = df["title"].fillna("").astype(str)
        description = df["description"].fillna("").astype(str)

        combined = (title + ". " + description).str.strip()

        combined = combined.str.replace(r"\s+", " ", regex=True)

        return combined
