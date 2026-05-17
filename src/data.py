import json
from pathlib import Path

import pandas as pd
import requests

WORLD_BANK_API = (
    "https://api.worldbank.org/v2/country/{countries}/indicator/NY.GDP.PCAP.KD"
)


def validate_dataset(df: pd.DataFrame) -> pd.DataFrame:
    required = {"country_code", "country_name", "year", "gdp_per_capita"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df = df.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["gdp_per_capita"] = pd.to_numeric(df["gdp_per_capita"], errors="coerce")
    df = df.dropna(subset=["year", "gdp_per_capita"])

    if df["gdp_per_capita"].le(0).any():
        raise ValueError("GDP per capita must be positive for all records.")

    df["country_code"] = df["country_code"].astype(str).str.strip()
    df["country_name"] = df["country_name"].astype(str).str.strip()
    df["year"] = df["year"].astype(int)
    df["gdp_per_capita"] = df["gdp_per_capita"].astype(float)

    if df["country_code"].nunique() < 2:
        raise ValueError("Dataset must contain data for at least two countries.")
    if df["year"].nunique() < 2:
        raise ValueError("Dataset must contain at least two distinct years.")

    return df[["country_code", "country_name", "year", "gdp_per_capita"]]


def load_local_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Local CSV file not found: {path}")
    df = pd.read_csv(path)
    df = df.rename(
        columns={
            "Country Code": "country_code",
            "Country Name": "country_name",
            "Year": "year",
            "GDP per capita": "gdp_per_capita",
        }
    )
    return validate_dataset(df)


def _parse_world_bank_json(response: dict, start_year: int, end_year: int) -> list[dict]:
    items = response[1]
    records = []
    for item in items:
        year = item.get("date")
        if year is None:
            continue
        year_int = int(year)
        if year_int < start_year or year_int > end_year:
            continue
        value = item.get("value")
        if value is None:
            continue
        country = item.get("country", {})
        records.append(
            {
                "country_code": country.get("id", "").strip(),
                "country_name": country.get("value", "").strip(),
                "year": year_int,
                "gdp_per_capita": value,
            }
        )
    return records


def fetch_world_bank_data(
    countries: list[str], start_year: int, end_year: int
) -> pd.DataFrame:
    if not countries:
        raise ValueError("At least one country code must be provided.")
    if start_year > end_year:
        raise ValueError("start_year must be less than or equal to end_year.")

    country_codes = ";".join(countries)
    url = WORLD_BANK_API.format(countries=country_codes)
    params = {"format": "json", "per_page": 20000, "date": f"{start_year}:{end_year}"}

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise RuntimeError("Failed to download World Bank data. Check your network or country codes.") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("Invalid response from World Bank API.") from exc

    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
        raise RuntimeError("Unexpected World Bank API response format.")

    records = _parse_world_bank_json(payload, start_year, end_year)
    if not records:
        raise RuntimeError("No GDP data found for the selected countries and years.")

    df = pd.DataFrame.from_records(records)
    return validate_dataset(df)
