from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import statsmodels.api as sm
except ImportError:  # pragma: no cover
    sm = None


def calculate_growth(df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for country_code, group in df.groupby("country_code", sort=False):
        group = group.sort_values("year")
        first = group.iloc[0]
        last = group.iloc[-1]
        years = last["year"] - first["year"]
        if years <= 0:
            raise ValueError("Country data must span at least two different years.")

        cagr = (last["gdp_per_capita"] / first["gdp_per_capita"]) ** (1 / years) - 1
        records.append(
            {
                "country_code": country_code,
                "country_name": first["country_name"],
                "initial_year": first["year"],
                "final_year": last["year"],
                "initial_gdp_per_capita": first["gdp_per_capita"],
                "final_gdp_per_capita": last["gdp_per_capita"],
                "average_annual_growth": cagr,
                "available_years": int(group["year"].nunique()),
            }
        )
    return pd.DataFrame.from_records(records)


def test_beta_convergence(growth_df: pd.DataFrame) -> dict[str, object]:
    if growth_df.empty:
        raise ValueError("Growth dataset is empty.")

    x = np.log(growth_df["initial_gdp_per_capita"].astype(float)).to_numpy()
    y = growth_df["average_annual_growth"].astype(float).to_numpy()
    x_with_const = np.column_stack([np.ones_like(x), x])

    coefficients, residuals, rank, s = np.linalg.lstsq(x_with_const, y, rcond=None)
    intercept, beta = float(coefficients[0]), float(coefficients[1])
    y_pred = x_with_const.dot(coefficients)
    ss_total = np.sum((y - y.mean()) ** 2)
    ss_res = np.sum((y - y_pred) ** 2)
    r_squared = float(1 - ss_res / ss_total) if ss_total > 0 else 0.0

    p_value = None
    if sm is not None:
        model = sm.OLS(y, x_with_const).fit()
        p_value = float(model.pvalues[1])

    # Generate detailed Polish interpretation
    if beta < 0:
        interpretation = (
            f"Obserwuje się beta-konwergencję (współczynnik β = {beta:.4f}). "
            f"Kraje o niższym początkowym PKB per capita rosły szybciej niż kraje bogatsze. "
            f"Współczynnik determinacji R² = {r_squared:.4f} sugeruje, że "
            f"około {r_squared*100:.1f}% zmienności tempa wzrostu można wyjaśnić początkowym poziomem dochodu. "
            f"To wskazuje na zjawisko doganiania biedniejszych krajów w stosunku do bogatszych, "
            f"co jest zgodne z przewidywaniami modelu Solowa."
        )
    else:
        interpretation = (
            f"Brak wyraźnej beta-konwergencji (współczynnik β = {beta:.4f}). "
            f"W badanej próbie biedniejsze kraje nie rosły szybciej od bogatszych. "
            f"To sugeruje, że różnice w początkowych dochodach nie są istotnym predyktorem "
            f"różnic w tempie wzrostu dla wybranych krajów."
        )

    return {
        "beta": beta,
        "intercept": intercept,
        "r_squared": r_squared,
        "p_value": p_value,
        "interpretation": interpretation,
    }


def test_sigma_convergence(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    if df.empty:
        raise ValueError("Dataset is empty.")

    df = df.copy()
    if (df["gdp_per_capita"] <= 0).any():
        raise ValueError("GDP per capita must be positive for sigma convergence calculations.")

    df["log_gdp"] = np.log(df["gdp_per_capita"].astype(float))
    sigma_df = (
        df.groupby("year", sort=True)["log_gdp"]
        .std()
        .reset_index()
        .rename(columns={"log_gdp": "sigma"})
    )
    first_sigma = float(sigma_df.iloc[0]["sigma"])
    last_sigma = float(sigma_df.iloc[-1]["sigma"])
    percentage_change = ((last_sigma - first_sigma) / first_sigma * 100) if first_sigma != 0 else float("inf")
    
    # Generate detailed Polish interpretation
    if last_sigma < first_sigma:
        interpretation = (
            f"Obserwuje się sigma-konwergencję. Rozproszenie dochodów (mierzone odchyleniem standardowym log PKB) "
            f"zmniejszyło się z {first_sigma:.4f} w roku {int(sigma_df.iloc[0]['year'])} "
            f"do {last_sigma:.4f} w roku {int(sigma_df.iloc[-1]['year'])}, "
            f"co stanowi zmianę o {percentage_change:.2f}%. "
            f"To oznacza, że różnice dochodowe między krajami zmniejszyły się, "
            f"a kraje stały się bardziej podobne pod względem dochodów per capita."
        )
    else:
        interpretation = (
            f"Brak sigma-konwergencji. Rozproszenie dochodów wzrosło z {first_sigma:.4f} "
            f"do {last_sigma:.4f}, co stanowi zmianę o {percentage_change:.2f}%. "
            f"Different dochodowe między krajami zwiększyły się, a nie zmniejszyły."
        )

    summary = {
        "first_year": int(sigma_df.iloc[0]["year"]),
        "last_year": int(sigma_df.iloc[-1]["year"]),
        "first_sigma": first_sigma,
        "last_sigma": last_sigma,
        "percentage_change": percentage_change,
        "interpretation": interpretation,
    }
    return sigma_df, summary
