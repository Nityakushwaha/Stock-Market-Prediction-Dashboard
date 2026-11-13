from __future__ import annotations

from typing import ClassVar

import pandas as pd

from src.validation.exceptions import ValidationError


class NewsValidator:
    """Validate user input and news DataFrames."""

    REQUIRED_COLUMNS: ClassVar[tuple[str, ...]] = (
        "company",
        "source",
        "author",
        "title",
        "description",
        "content",
        "url",
        "published_at",
    )

    @staticmethod
    def validate_query(query: str) -> str:
        if not isinstance(query, str):
            raise ValidationError("Query must be a string.")

        query = query.strip()

        if not query:
            raise ValidationError("Query cannot be empty.")

        return query

    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            raise ValidationError("No news articles were returned.")

        missing = [
            column for column in cls.REQUIRED_COLUMNS if column not in df.columns
        ]

        if missing:
            raise ValidationError(f"Missing required columns: {missing}")

        df = df.copy()

        df.drop_duplicates(
            subset=["url"],
            inplace=True,
            ignore_index=True,
        )

        df["title"] = df["title"].fillna("").astype(str).str.strip()

        df = df[df["title"] != ""].reset_index(drop=True)

        return df
