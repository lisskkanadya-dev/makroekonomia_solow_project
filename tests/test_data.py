import json
from pathlib import Path

import pandas as pd
import pytest
import requests

from src.data import fetch_world_bank_data, load_local_csv, validate_dataset

SAMPLE_CSV = "country_code,country_name,year,gdp_per_capita\nPOL,Poland,2000,10000\nPOL,Poland,2020,20000\nDEU,Germany,2000,40000\nDEU,Germany,2020,50000\nROU,Romania,2000,5000\nROU,Romania,2020,18000\n"


def test_load_local_csv_reads_dataframe(tmp_path: Path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(SAMPLE_CSV, encoding="utf-8")

    df = load_local_csv(csv_path)

    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == {"country_code", "country_name", "year", "gdp_per_capita"}
    assert len(df) == 6


def test_validate_dataset_rejects_missing_columns():
    df = pd.DataFrame({"country_code": ["POL"], "year": [2000]})
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_dataset(df)


def test_load_local_csv_drops_missing_gdp(tmp_path: Path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(
        "country_code,country_name,year,gdp_per_capita\nPOL,Poland,2000,\nDEU,Germany,2000,40000\nPOL,Poland,2020,20000\n", encoding="utf-8"
    )
    df = load_local_csv(csv_path)
    assert len(df) == 2
    assert set(df["country_code"]) == {"POL", "DEU"}


def test_validate_dataset_rejects_fewer_than_two_countries(tmp_path: Path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("country_code,country_name,year,gdp_per_capita\nPOL,Poland,2000,10000\nPOL,Poland,2020,20000\n", encoding="utf-8")
    with pytest.raises(ValueError, match="at least two countries"):
        load_local_csv(csv_path)


def test_validate_dataset_rejects_fewer_than_two_years(tmp_path: Path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("country_code,country_name,year,gdp_per_capita\nPOL,Poland,2000,10000\nDEU,Germany,2000,40000\n", encoding="utf-8")
    with pytest.raises(ValueError, match="at least two distinct years"):
        load_local_csv(csv_path)


def test_fetch_world_bank_data_parses_api(monkeypatch):
    sample_response = [
        {"page": 1, "total": 1},
        [
            {
                "date": "2000",
                "value": 10000,
                "country": {"id": "POL", "value": "Poland"},
            },
            {
                "date": "2020",
                "value": 20000,
                "country": {"id": "POL", "value": "Poland"},
            },
            {
                "date": "2000",
                "value": 40000,
                "country": {"id": "DEU", "value": "Germany"},
            },
            {
                "date": "2020",
                "value": 50000,
                "country": {"id": "DEU", "value": "Germany"},
            },
        ],
    ]

    class DummyResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return sample_response

    def fake_get(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr(requests, "get", fake_get)
    df = fetch_world_bank_data(["POL", "DEU"], 2000, 2020)

    assert set(df.columns) == {"country_code", "country_name", "year", "gdp_per_capita"}
    assert len(df) == 4
    assert df["country_code"].tolist() == ["POL", "POL", "DEU", "DEU"]


def test_fetch_world_bank_data_network_error_is_runtime_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.RequestException("connection failed")

    monkeypatch.setattr(requests, "get", fake_get)
    with pytest.raises(RuntimeError, match="Failed to download World Bank data"):
        fetch_world_bank_data(["POL"], 2000, 2020)
