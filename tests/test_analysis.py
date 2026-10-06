import pandas as pd
import pytest

from src.analysis import (
    add_rent_growth,
    add_tightness_indicators,
    change_since,
    tightness_summary,
)


@pytest.fixture
def sample():
    return pd.DataFrame(
        {
            "city": ["A", "A", "A", "B", "B", "B"],
            "year": [2020, 2021, 2022, 2020, 2021, 2022],
            "avg_rent_2br": [1000.0, 1100.0, 1210.0, 800.0, 840.0, 1008.0],
            "vacancy_rate": [3.5, 2.0, 1.0, 4.0, 3.0, 2.5],
            "all_cma_vacancy_rate": [3.0, 2.5, 2.0, 3.0, 2.5, 2.0],
        }
    )


def test_rent_growth(sample):
    out = add_rent_growth(sample)
    a_2021 = out[(out.city == "A") & (out.year == 2021)].iloc[0]
    assert a_2021["rent_growth_pct"] == pytest.approx(10.0)  # 1100 / 1000
    assert pd.isna(out[(out.city == "A") & (out.year == 2020)].iloc[0]["rent_growth_pct"])


def test_change_since(sample):
    out = change_since(sample, "avg_rent_2br", 2020)
    b_2022 = out[(out.city == "B") & (out.year == 2022)].iloc[0]
    assert b_2022["avg_rent_2br_change_pct"] == pytest.approx(26.0)  # 1008 / 800


def test_tightness_indicators(sample):
    out = add_tightness_indicators(sample)
    a_2022 = out[(out.city == "A") & (out.year == 2022)].iloc[0]
    assert a_2022["vacancy_gap_pts"] == pytest.approx(-1.0)  # 1.0 - 2.0
    assert bool(a_2022["below_balanced"]) is True
    b_2020 = out[(out.city == "B") & (out.year == 2020)].iloc[0]
    assert bool(b_2020["below_balanced"]) is False  # 4.0 >= 3.0


def test_tightness_summary(sample):
    s = tightness_summary(sample, 2020)
    assert s.loc["A", "years_below_balanced"] == 2  # 2.0 and 1.0 are below 3.0
    assert s.loc["A", "min_vacancy_year"] == 2022
    assert s.loc["B", "rent_change_pct"] == pytest.approx(26.0)
