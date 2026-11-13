from __future__ import annotations

import unittest

import pandas as pd

from src.analytics.growth_labels import add_12_month_growth_labels


class GrowthLabelTests(unittest.TestCase):
    def test_labels_use_first_trading_day_on_or_after_anniversary(self) -> None:
        prices = pd.DataFrame(
            {
                "date": [
                    "2021-01-04",
                    "2020-01-03",
                    "2021-01-02",
                    "2020-01-02",
                ],
                "ticker": ["INFY"] * 4,
                "adjusted_close": [90.0, 200.0, 110.0, 100.0],
            }
        )

        result = add_12_month_growth_labels(prices)
        by_date = result.set_index("date")

        positive_row = by_date.loc[pd.Timestamp("2020-01-02")]
        negative_row = by_date.loc[pd.Timestamp("2020-01-03")]

        self.assertAlmostEqual(positive_row["forward_return_12m"], 0.10)
        self.assertEqual(positive_row["growth_label"], "positive")
        self.assertAlmostEqual(negative_row["forward_return_12m"], -0.55)
        self.assertEqual(negative_row["growth_label"], "negative")

    def test_missing_or_too_distant_target_price_stays_unlabeled(self) -> None:
        prices = pd.DataFrame(
            {
                "date": ["2020-01-01", "2021-01-20"],
                "ticker": ["INFY", "INFY"],
                "adjusted_close": [100.0, 110.0],
            }
        )

        result = add_12_month_growth_labels(prices)

        self.assertTrue(pd.isna(result.loc[0, "forward_return_12m"]))
        self.assertTrue(pd.isna(result.loc[0, "growth_label"]))
        self.assertTrue(pd.isna(result.loc[1, "growth_label"]))

    def test_zero_return_is_labeled_negative(self) -> None:
        prices = pd.DataFrame(
            {
                "date": ["2020-01-01", "2021-01-01"],
                "ticker": ["INFY", "INFY"],
                "adjusted_close": [100.0, 100.0],
            }
        )

        result = add_12_month_growth_labels(prices)

        self.assertEqual(result.loc[0, "forward_return_12m"], 0.0)
        self.assertEqual(result.loc[0, "growth_label"], "negative")

    def test_rejects_duplicate_ticker_dates(self) -> None:
        prices = pd.DataFrame(
            {
                "date": ["2020-01-01", "2020-01-01"],
                "ticker": ["INFY", "INFY"],
                "adjusted_close": [100.0, 101.0],
            }
        )

        with self.assertRaisesRegex(ValueError, "at most one price per date"):
            add_12_month_growth_labels(prices)


if __name__ == "__main__":
    unittest.main()
