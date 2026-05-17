from pathlib import Path

import pandas as pd

from src.charts import create_beta_chart, create_gdp_chart, create_sigma_chart

SAMPLE_DATA = {
    "country_code": ["POL", "POL", "DEU", "DEU"],
    "country_name": ["Poland", "Poland", "Germany", "Germany"],
    "year": [2000, 2020, 2000, 2020],
    "gdp_per_capita": [10000, 20000, 40000, 50000],
}

SAMPLE_GROWTH = {
    "country_code": ["POL", "DEU"],
    "country_name": ["Poland", "Germany"],
    "initial_year": [2000, 2000],
    "final_year": [2020, 2020],
    "initial_gdp_per_capita": [10000.0, 40000.0],
    "final_gdp_per_capita": [20000.0, 50000.0],
    "average_annual_growth": [0.035, 0.011],
    "available_years": [2, 2],
}


def test_create_gdp_chart_file_is_created(tmp_path: Path):
    df = pd.DataFrame(SAMPLE_DATA)
    path = create_gdp_chart(df, tmp_path)

    assert path.exists()
    assert path.suffix == ".png"


def test_create_beta_chart_file_is_created(tmp_path: Path):
    df = pd.DataFrame(SAMPLE_GROWTH)
    beta_result = {"beta": -0.5, "intercept": 0.1, "r_squared": 0.8}
    path = create_beta_chart(df, beta_result, tmp_path)

    assert path.exists()
    assert path.name == "beta_convergence.png"


def test_create_sigma_chart_file_is_created(tmp_path: Path):
    sigma_df = pd.DataFrame({"year": [2000, 2020], "sigma": [0.4, 0.3]})
    path = create_sigma_chart(sigma_df, tmp_path)

    assert path.exists()
    assert path.name == "sigma_convergence.png"
