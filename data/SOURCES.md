# Data sources

**Scope**: Moncton and Saint John (2020 to 2025). Fredericton is out of scope because it is missing from the vacancy table (see section 2).

Data files are not versioned. This file explains where to download them and how to build `data/processed/housing_tidy.csv`.

## 1. Average rents: Statistics Canada (CMHC data)

**Table 34-10-0133-01**: "Canada Mortgage and Housing Corporation, average rents for areas with a population of 10,000 and over". Annual data by structure type and number of bedrooms (studio, 1, 2, 3+ bedrooms).
https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3410013301

- Filter: geography = Moncton, Saint John; unit type = 2 bedrooms; years = 2020 to the latest.
- Check the last update date shown on the table page.
- Use **the same geography for every city** (CMA or census subdivision) and note it in the README.
- **Found in the downloaded file**: 244 geographies; Moncton, Fredericton and Saint John are all present, with years 1987 to 2025. Four structure types exist; the project keeps "row and apartment structures of three units and over" (French label: "Logements en bandes et immeubles d'appartements de trois logements et plus"), the only total that is complete for the three cities from 2020 to 2025. The apartment-only total gives almost the same values.

## 2. Vacancy rates: Statistics Canada (CMHC data)

**Table 34-10-0130-01**: CMHC vacancy rates for census metropolitan areas (CMAs), including Moncton and Saint John.
https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3410013001

- **Found in the downloaded file**: 37 regions, including Moncton and Saint John but **not Fredericton**. Its vacancy rate has to come from another CMHC source (the HMIP portal or the Excel tables in section 2b), making sure the geography matches (the HMIP portal shows Fredericton at the census subdivision level).
- Filter on Moncton and Saint John and the same years as the rents. The row "Régions métropolitaines de recensement" (all CMAs together) is kept as a **benchmark**.

**Alternative / cross-check**: the CMHC portal (HMIP) offers the same series with CSV export, for example for Moncton:
https://www03.cmhc-schl.gc.ca/hmip-pimh/en/TableMapChart/Table?TableId=2.2.15&GeographyId=1040&GeographyTypeId=3&DisplayAs=Table&GeograghyName=Moncton

## 2b. Complement: CMHC Rental Market Survey Excel tables

CMHC publishes the 2025 Rental Market Survey tables in Excel (vacancy, average rents, turnover, universe) for Canada, the provinces and major centres:
https://www.cmhc-schl.gc.ca/professionals/housing-markets-data-and-research/housing-data/data-tables/rental-market/rental-market-report-data-tables

- **Role in the project**: complementary source, useful to validate the 2025 figures obtained from the Statistics Canada tables.
- **Historical coverage to check**: the page mentions tables for 2019 to 2025, which could be enough for an analysis since 2020. Open the file to confirm whether it holds earlier years or only 2025, and whether Moncton, Fredericton and Saint John are included.

## 3. Household income (optional extension, not used now)

Income is not needed for the current question. It would be needed to add an affordability analysis (rent-to-income ratio). Leads to check:

- **T1 Family File (T1FF)** from Statistics Canada: annual estimates of family income by CMA. The *Daily* releases publish median total income of census families by CMA. The matching data table number still has to be found on the Statistics Canada site; I have not confirmed it.
- **2016 and 2021 censuses** (incomes of 2015 and 2020): reliable, but only two points in time.
- The CMHC portal also offers a "Household Income - Average and Median" table by region.

Note: median income of **census families** (T1FF) is not the same as median income of **households** (census). Pick one measure, name it in the notebook and explain the difference in the limitations.

## 4. Building housing_tidy.csv

One row per city and year, with these columns:

| Column | Description |
|---|---|
| `city` | Moncton, Saint John |
| `year` | Survey year (October) |
| `avg_rent_2br` | Average monthly rent, 2-bedroom apartment ($) |
| `vacancy_rate` | Vacancy rate of the city (%) |
| `all_cma_vacancy_rate` | Vacancy rate of all CMAs together (%), used as a benchmark |

Run `python -m src.build_tidy` to produce it from the raw files, then open the notebook.
