import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src import analysis as analysis_module
from src.analysis import calculate_growth

SAMPLE_DATA = {
    "country_code": ["POL", "POL", "DEU", "DEU", "ROU", "ROU"],
    "country_name": ["Poland", "Poland", "Germany", "Germany", "Romania", "Romania"],
    "year": [2000, 2020, 2000, 2020, 2000, 2020],
    "gdp_per_capita": [10000, 20000, 40000, 50000, 5000, 18000],
}


def test_calculate_growth_computes_cagr_correctly():
    df = pd.DataFrame(SAMPLE_DATA)
    growth_df = calculate_growth(df)
    pol = growth_df[growth_df["country_code"] == "POL"].iloc[0]

    assert math.isclose(pol["initial_gdp_per_capita"], 10000.0)
    assert math.isclose(pol["final_gdp_per_capita"], 20000.0)
    assert math.isclose(pol["average_annual_growth"], (20000 / 10000) ** (1 / 20) - 1)


def test_calculate_growth_selects_first_and_last_year():
    df = pd.DataFrame({
        "country_code": ["POL", "POL", "POL"],
        "country_name": ["Poland"] * 3,
        "year": [2000, 2010, 2020],
        "gdp_per_capita": [10000, 15000, 20000],
    })
    growth_df = calculate_growth(df)
    assert growth_df.iloc[0]["initial_year"] == 2000
    assert growth_df.iloc[0]["final_year"] == 2020


def test_beta_convergence_returns_negative_beta_for_sample_dataset():
    df = pd.DataFrame(SAMPLE_DATA)
    growth_df = analysis_module.calculate_growth(df)
    result = analysis_module.test_beta_convergence(growth_df)

    assert "beta" in result
    assert "r_squared" in result
    assert result["beta"] < 0
    assert "beta-konwergencj" in result["interpretation"].lower()


def test_sigma_convergence_calculates_dispersion_each_year():
    df = pd.DataFrame(SAMPLE_DATA)
    sigma_df, summary = analysis_module.test_sigma_convergence(df)

    assert list(sigma_df.columns) == ["year", "sigma"]
    assert summary["first_year"] == 2000
    assert summary["last_year"] == 2020
    assert isinstance(summary["percentage_change"], float)


def test_sigma_convergence_detects_decreasing_dispersion():
    df = pd.DataFrame(SAMPLE_DATA)
    sigma_df, summary = analysis_module.test_sigma_convergence(df)
    assert summary["last_sigma"] < summary["first_sigma"]


def test_analysis_handles_missing_middle_years():
    df = pd.DataFrame({
        "country_code": ["POL", "POL", "DEU", "DEU"],
        "country_name": ["Poland", "Poland", "Germany", "Germany"],
        "year": [2000, 2020, 2000, 2020],
        "gdp_per_capita": [10000, 19000, 40000, 51000],
    })
    growth_df = analysis_module.calculate_growth(df)
    sigma_df, summary = analysis_module.test_sigma_convergence(df)
    assert len(growth_df) == 2
    assert len(sigma_df) == 2
    assert summary["interpretation"]


def test_sigma_convergence_rejects_non_positive_gdp():
    df = pd.DataFrame({
        "country_code": ["POL", "DEU"],
        "country_name": ["Poland", "Germany"],
        "year": [2000, 2000],
        "gdp_per_capita": [10000, -500.0],
    })
    with pytest.raises(ValueError, match="GDP per capita must be positive"):
        analysis_module.test_sigma_convergence(df)
