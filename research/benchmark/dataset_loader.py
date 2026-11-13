from __future__ import annotations

import pandas as pd

from src.models import Company


def load_companies(path: str) -> list[Company]:
    """Load benchmark companies from a CSV file."""

    df = pd.read_csv(path)

    companies = []

    for _, row in df.iterrows():
        companies.append(
            Company(
                ticker=row["ticker"],
                company=row["company"],
                country=row["country"],
                sector=row["sector"],
                aliases=[alias.strip() for alias in row["aliases"].split(",")],
            )
        )

    return companies