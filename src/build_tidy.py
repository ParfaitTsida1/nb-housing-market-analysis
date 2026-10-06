"""Build the working tables from the raw Statistics Canada files.

Inputs (in data/raw/, ";" separator, UTF-8 with BOM):
  - 34100133*.csv: CMHC average rents (table 34-10-0133-01)
  - 34100130*.csv: CMHC vacancy rates (table 34-10-0130-01)

Outputs (in data/processed/):
  - housing_tidy.csv      : one row per city (Moncton, Saint John) and year
  - rents_by_bedroom.csv  : average rents by number of bedrooms

Usage: python -m src.build_tidy
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"

START_YEAR = 2020

# Scope: the two largest cities of southern New Brunswick.
# (Fredericton is out of scope: it is missing from the vacancy table.)
CITIES = {
    "Moncton, Nouveau-Brunswick": "Moncton",
    "Saint John, Nouveau-Brunswick": "Saint John",
}

# Benchmark row of the vacancy table: all census metropolitan areas together
ALL_CMA_LABEL = "Régions métropolitaines de recensement"

# Structure type kept: the only total that is complete for both cities, 2020-2025
STRUCTURE = (
    "Logements en bandes et immeubles d'appartements de trois logements et plus"
)

BEDROOMS = {
    "Studios": "studio",
    "Logements d'une chambre": "1_bedroom",
    "Logements de deux chambres": "2_bedroom",
    "Logements de trois chambres": "3_bedroom",
}


def _read(pattern: str) -> pd.DataFrame:
    files = sorted(DATA_RAW.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No file matching {pattern} in {DATA_RAW}")
    return pd.read_csv(files[0], sep=";", encoding="utf-8-sig", dtype=str)


def load_rents() -> pd.DataFrame:
    df = _read("34100133*.csv")
    df = df[df["GÉO"].isin(CITIES) & (df["Type de structure"] == STRUCTURE)].copy()
    df["city"] = df["GÉO"].map(CITIES)
    df["year"] = df["PÉRIODE DE RÉFÉRENCE"].astype(int)
    df["bedrooms"] = df["Type d'unité"].map(BEDROOMS)
    df["avg_rent"] = pd.to_numeric(df["VALEUR"], errors="coerce")
    df = df[df["year"] >= START_YEAR]
    return df[["city", "year", "bedrooms", "avg_rent"]].sort_values(
        ["city", "year", "bedrooms"]
    )


def load_vacancy() -> pd.DataFrame:
    df = _read("34100130*.csv")
    df = df[df["GÉO"].isin(CITIES)].copy()
    df["city"] = df["GÉO"].map(CITIES)
    df["year"] = df["PÉRIODE DE RÉFÉRENCE"].astype(int)
    df["vacancy_rate"] = pd.to_numeric(df["VALEUR"], errors="coerce")
    df = df[df["year"] >= START_YEAR]
    return df[["city", "year", "vacancy_rate"]]


def load_all_cma_vacancy() -> pd.DataFrame:
    """Vacancy rate for all census metropolitan areas together (benchmark)."""
    df = _read("34100130*.csv")
    df = df[df["GÉO"] == ALL_CMA_LABEL].copy()
    df["year"] = df["PÉRIODE DE RÉFÉRENCE"].astype(int)
    df["all_cma_vacancy_rate"] = pd.to_numeric(df["VALEUR"], errors="coerce")
    return df[df["year"] >= START_YEAR][["year", "all_cma_vacancy_rate"]]


def build():
    rents = load_rents()
    vacancy = load_vacancy()
    benchmark = load_all_cma_vacancy()

    two_br = (
        rents[rents["bedrooms"] == "2_bedroom"]
        .rename(columns={"avg_rent": "avg_rent_2br"})
        .drop(columns="bedrooms")
    )

    # Full city x year grid, so missing values show up explicitly
    years = range(START_YEAR, int(rents["year"].max()) + 1)
    grid = pd.MultiIndex.from_product(
        [list(CITIES.values()), years], names=["city", "year"]
    ).to_frame(index=False)

    tidy = (
        grid.merge(two_br, on=["city", "year"], how="left")
        .merge(vacancy, on=["city", "year"], how="left")
        .merge(benchmark, on="year", how="left")
        .sort_values(["city", "year"])
        .reset_index(drop=True)
    )

    assert not tidy.duplicated(["city", "year"]).any(), "Duplicate city/year rows"
    assert tidy["avg_rent_2br"].notna().all(), "Missing 2-bedroom rents"
    assert tidy["vacancy_rate"].notna().all(), "Missing vacancy rates"
    assert tidy["all_cma_vacancy_rate"].notna().all(), "Missing benchmark"
    return tidy, rents


if __name__ == "__main__":
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    tidy, rents = build()
    tidy.to_csv(DATA_PROCESSED / "housing_tidy.csv", index=False)
    rents.to_csv(DATA_PROCESSED / "rents_by_bedroom.csv", index=False)
    print(tidy.to_string(index=False))
    print("\nMissing values:")
    print(tidy.isna().sum())
