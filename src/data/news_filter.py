from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from config.universe import NIFTY_RESEARCH_UNIVERSE


def _normalize_text(series: pd.Series) -> pd.Series:
    """Normalize headline text for deterministic matching."""
    return (
        series.astype(str)
        .str.lower()
        .str.replace("&", " and ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def _alias_pattern(alias: str) -> str:
    """Create a word-boundary-safe regex for an alias."""
    normalized = alias.lower().replace("&", " and ")
    return rf"(?<!\w){re.escape(normalized)}(?!\w)"


def load_economic_times(
    directory: str | Path,
) -> pd.DataFrame:
    """Load all Economic Times CSV files from a directory."""

    directory = Path(directory)

    files = sorted(
        directory.glob("economic_times_headlines_*.csv")
    )

    if not files:
        raise FileNotFoundError(
            f"No Economic Times CSV files found in {directory}"
        )

    frames = [
        pd.read_csv(
            file,
            usecols=["Date", "Headline", "Headline link"],
        )
        for file in files
    ]

    result = pd.concat(
        frames,
        ignore_index=True,
    )

    result["Date"] = pd.to_datetime(
        result["Date"],
        format="%d-%m-%Y",
        errors="raise",
    )

    return result


def filter_news(
    news_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Match Economic Times headlines against the research universe.

    One headline may map to multiple companies when multiple explicit
    company entities appear in the headline.
    """

    required_columns = {
        "Date",
        "Headline",
        "Headline link",
    }

    missing = required_columns - set(news_df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    headlines = _normalize_text(news_df["Headline"])

    records: list[pd.DataFrame] = []

    for ticker, metadata in NIFTY_RESEARCH_UNIVERSE.items():

        aliases = metadata["aliases"]

        if not aliases:
            continue

        pattern = "|".join(
            _alias_pattern(alias)
            for alias in aliases
        )

        mask = headlines.str.contains(
            pattern,
            regex=True,
            na=False,
        )

        if not mask.any():
            continue

        matched = news_df.loc[
            mask,
            ["Date", "Headline", "Headline link"],
        ].copy()

        matched["ticker"] = ticker

        matched_alias = headlines.loc[mask].map(
            lambda text: next(
                (
                    alias
                    for alias in aliases
                    if re.search(
                        _alias_pattern(alias),
                        text,
                    )
                ),
                None,
            )
        )

        matched["matched_alias"] = matched_alias.values

        matched["match_method"] = "headline_alias"

        matched = matched.rename(
            columns={
                "Date": "date",
                "Headline": "headline",
                "Headline link": "url",
            }
        )

        records.append(matched)

    if not records:
        return pd.DataFrame(
            columns=[
                "date",
                "ticker",
                "headline",
                "url",
                "match_method",
                "matched_alias",
            ]
        )

    result = pd.concat(
        records,
        ignore_index=True,
    )

    result = result.drop_duplicates(
        subset=["ticker", "url"]
    )

    return result[
        [
            "date",
            "ticker",
            "headline",
            "url",
            "match_method",
            "matched_alias",
        ]
    ].reset_index(drop=True)