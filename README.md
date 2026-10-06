# Rents, Vacancy and Rental-Market Tightness in Southern New Brunswick (using Claude AI assistance)

Analysis of how the rental market has evolved in **Moncton and Saint John** since 2020.

## Research question

> How have rents and vacancy rates changed in Moncton and Saint John since 2020, and what does this reveal about the tightness of the rental market in the two largest cities of southern New Brunswick?

## Method

1. **Data**: average rents (table 34-10-0133-01) and vacancy rates (table 34-10-0130-01) from CMHC, published by Statistics Canada (see `data/SOURCES.md`).
2. **Cleaning**: a tidy table (one row per city and year) built into `data/processed/housing_tidy.csv` by `src/build_tidy.py`.
3. **Analysis** (`notebooks/01_rent_vacancy_tightness.ipynb`):
   - evolution of the average rent of a 2-bedroom apartment;
   - evolution of the vacancy rate, compared with the all-CMA vacancy rate and with the 3% rule of thumb for a balanced market;
   - year-over-year rent growth;
   - a tightness summary per city.
4. **Conclusion**: what rents and vacancy together say about market tightness in each city.

## Results

Average monthly rent, 2-bedroom apartment (CMHC, October survey):

| City | 2020 | 2025 | Change |
|---|---|---|---|
| Moncton | $949 | $1,452 | +53.0% |
| Saint John | $825 | $1,290 | +56.4% |

Vacancy rate:

| City | 2020 | Low | 2025 | Years below 3% |
|---|---|---|---|---|
| Moncton | 2.8% | 1.2% (2023) | 3.8% | 5 of 6 |
| Saint John | 3.0% | 1.7% (2022) | 2.1% | 4 of 6 |

- Rents rose about 9% a year on average in both cities.
- Both markets were tight for most of the period (vacancy below 3% in most years, and Moncton down to 1.2% in 2023).
- In 2025, rent growth slowed in both cities (Moncton +6.4%, Saint John +5.0%, the lowest of the period). Moncton's vacancy rate rose to 3.8%, above the all-CMA benchmark (3.1%), a first sign of easing; Saint John's is back to 2.1%, still tighter than the benchmark.
- Rents kept rising even when vacancy was above 3% (Saint John in 2024: vacancy 3.9%, rent +12.4%), so a higher vacancy rate does not by itself mean falling rents.

Figures are in `reports/figures/`.

## Limitations

- CMHC average rent reflects existing units, not the asking rent of new listings.
- Only six yearly observations per city: the results describe a pattern but cannot support statistical tests or causal claims.
- Structure type kept: row and apartment structures of three units and over (the only total that is complete for both cities from 2020 to 2025). Results are almost identical with apartment structures of three units and over.
- A single unit type (2-bedroom) is used for the main comparison; other sizes are in `data/processed/rents_by_bedroom.csv`.
- The 3% vacancy threshold is a rule of thumb, not an official threshold; a source should be cited before relying on it.
- Affordability (rent relative to income) is not covered: it would need income data by city.
- Fredericton is out of scope because it is missing from the vacancy table (table 34-10-0130-01).

## Project structure

```
data/raw/         Raw downloaded data (not versioned)
data/processed/   Cleaned tables housing_tidy.csv and rents_by_bedroom.csv (not versioned)
data/SOURCES.md   Sources and steps to rebuild the data
notebooks/        Analysis notebook
src/build_tidy.py Builds the working tables from the raw files
src/analysis.py   Reusable functions (rent growth, tightness indicators)
tests/            Tests for the functions
reports/figures/  Exported charts
```

## Running the project

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
# put the two Statistics Canada CSV files in data/raw/
python -m src.build_tidy
jupyter lab
```

Run the tests with `pytest`.

## Tools

Python, pandas, matplotlib, Jupyter.

## Possible extensions

- Add Fredericton once a comparable vacancy series is found.
- Add affordability (rent-to-income ratio) with income data by city.
- Compare with another regional city, such as Halifax.
