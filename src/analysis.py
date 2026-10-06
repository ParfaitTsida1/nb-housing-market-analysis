"""Reusable functions for the rent and rental-market tightness analysis.

Expected tidy file (data/processed/housing_tidy.csv), one row per city and year:

    city, year, avg_rent_2br, vacancy_rate, all_cma_vacancy_rate

- avg_rent_2br: average monthly rent of a 2-bedroom unit ($)
- vacancy_rate: vacancy rate of the city (%)
- all_cma_vacancy_rate: vacancy rate of all census metropolitan areas (%),
  used as a benchmark
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"

REQUIRED_COLUMNS = [
    "city",
    "year",
    "avg_rent_2br",
    "vacancy_rate",
    "all_cma_vacancy_rate",
]

# Rule-of-thumb vacancy rate for a balanced rental market (a convention, not an
# official threshold). Below it the market is usually described as tight.
BALANCED_VACANCY_PCT = 3.0


def load_tidy(name: str = "housing_tidy.csv") -> pd.DataFrame:
    """Load the tidy file from data/processed and check its columns."""
    df = pd.read_csv(DATA_PROCESSED / name)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df


def add_rent_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Add the year-over-year rent growth (%), computed per city."""
    out = df.sort_values(["city", "year"]).copy()
    out["rent_growth_pct"] = out.groupby("city")["avg_rent_2br"].pct_change() * 100
    return out


def change_since(df: pd.DataFrame, column: str, base_year: int) -> pd.DataFrame:
    """Percent change of `column` versus `base_year`, computed per city."""
    base = (
        df[df["year"] == base_year].set_index("city")[column].rename("base_value")
    )
    out = df.join(base, on="city")
    out[f"{column}_change_pct"] = (out[column] / out["base_value"] - 1) * 100
    return out.drop(columns="base_value")


def add_tightness_indicators(
    df: pd.DataFrame, threshold: float = BALANCED_VACANCY_PCT
) -> pd.DataFrame:
    """Add vacancy-based tightness indicators.

    - vacancy_gap_pts: city vacancy minus the all-CMA benchmark (points);
      negative means tighter than the benchmark.
    - below_balanced: True when the vacancy rate is under `threshold`.
    """
    out = df.copy()
    out["vacancy_gap_pts"] = out["vacancy_rate"] - out["all_cma_vacancy_rate"]
    out["below_balanced"] = out["vacancy_rate"] < threshold
    return out


def tightness_summary(df: pd.DataFrame, base_year: int) -> pd.DataFrame:
    """One-row-per-city summary of rent growth and vacancy over the period."""
    d = add_rent_growth(add_tightness_indicators(df))
    rows = []
    for city, g in d.groupby("city"):
        g = g.sort_values("year")
        first, last = g.iloc[0], g.iloc[-1]
        rows.append(
            {
                "city": city,
                "rent_change_pct": (last["avg_rent_2br"] / first["avg_rent_2br"] - 1)
                * 100,
                "avg_yearly_rent_growth_pct": g["rent_growth_pct"].mean(),
                "avg_vacancy_pct": g["vacancy_rate"].mean(),
                "min_vacancy_pct": g["vacancy_rate"].min(),
                "min_vacancy_year": int(g.loc[g["vacancy_rate"].idxmin(), "year"]),
                "years_below_balanced": int(g["below_balanced"].sum()),
                "years_total": int(len(g)),
                "latest_vacancy_pct": last["vacancy_rate"],
                "latest_gap_vs_cma_pts": last["vacancy_gap_pts"],
            }
        )
    return pd.DataFrame(rows).set_index("city")
