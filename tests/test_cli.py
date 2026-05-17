import sys
from pathlib import Path

import pytest

from src import solow_app

SAMPLE_CSV = "country_code,country_name,year,gdp_per_capita\nPOL,Poland,2000,10000\nPOL,Poland,2020,20000\nDEU,Germany,2000,40000\nDEU,Germany,2020,50000\n"


def test_cli_runs_successfully_with_offline_data(tmp_path: Path, monkeypatch):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(SAMPLE_CSV, encoding="utf-8")
    output_dir = tmp_path / "site"

    monkeypatch.setattr(sys, "argv", ["solow_app", "--offline-data", str(csv_path), "--output-dir", str(output_dir)])
    result = solow_app.main()

    assert result == 0
    assert (output_dir / "index.html").exists()
    assert (output_dir / "gdp_per_capita.png").exists()
    assert (output_dir / "beta_convergence.png").exists()
    assert (output_dir / "sigma_convergence.png").exists()


def test_cli_returns_non_zero_for_invalid_input(tmp_path: Path, monkeypatch):
    invalid_csv = tmp_path / "missing.csv"
    monkeypatch.setattr(sys, "argv", ["solow_app", "--offline-data", str(invalid_csv), "--output-dir", str(tmp_path / "site")])

    result = solow_app.main()
    assert result != 0
