from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_gdp_chart(df: pd.DataFrame, output_dir: Path | str) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "gdp_per_capita.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    for country_code, group in df.groupby("country_code"):
        ax.plot(group["year"], group["gdp_per_capita"], marker="o", label=country_code)

    ax.set_title("GDP per Capita over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("GDP per Capita (constant 2015 USD)")
    ax.legend(title="Country")
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def create_beta_chart(growth_df: pd.DataFrame, beta_result: dict[str, object], output_dir: Path | str) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "beta_convergence.png"

    x = np.log(growth_df["initial_gdp_per_capita"].astype(float))
    y = growth_df["average_annual_growth"].astype(float)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, color="tab:blue", label="Countries")
    if growth_df.shape[0] >= 2:
        beta = float(beta_result["beta"])
        intercept = float(beta_result["intercept"])
        x_line = np.linspace(x.min(), x.max(), 100)
        ax.plot(x_line, intercept + beta * x_line, color="tab:red", label="Regression line")

    ax.set_title("Beta-Convergence: Growth vs Initial GDP")
    ax.set_xlabel("Log initial GDP per capita")
    ax.set_ylabel("Average annual growth rate")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def create_sigma_chart(sigma_df: pd.DataFrame, output_dir: Path | str) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "sigma_convergence.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sigma_df["year"], sigma_df["sigma"], marker="o", color="tab:green")
    ax.set_title("Sigma-Convergence: Dispersion of Log GDP per Capita")
    ax.set_xlabel("Year")
    ax.set_ylabel("Sigma (standard deviation of log GDP)")
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path
