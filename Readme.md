# Solow Model Convergence Project

This repository implements a lightweight Python application that tests empirical predictions of the Solow growth model using GDP per capita data.

The generated report is in **Polish language** (Raport w języku polskim).

## What it does

- downloads GDP per capita data from the World Bank API,
- calculates average annual GDP per capita growth,
- tests beta-convergence and sigma-convergence,
- generates charts as PNG files,
- builds a static HTML report in `site/index.html`.

## Run the project

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.solow_app --output-dir site
```

## Offline data mode

```powershell
python -m src.solow_app --offline-data data/sample.csv --output-dir site
```

## Tests

```powershell
pytest
```