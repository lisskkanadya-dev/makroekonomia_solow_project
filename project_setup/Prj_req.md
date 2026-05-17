# Wymagania Techniczne: Model Solowa i Test Empiryczny Konwergencji

## 1. Przegląd projektu

Projekt jest lekką aplikacją Python dla celów akademickich. Automatycznie pobiera dane o PKB per capita dla wybranych krajów, oblicza wskaźniki wzrostu, sprawdza beta-konwergencję i sigma-konwergencję, generuje wykresy i prezentuje wnioski zrozumiałe dla odbiorcy.

Projekt powinien być odpowiedni do wdrożenia na GitHub Pages za pomocą GitHub Actions. Końcowy wynik powinien być dostępny jako statyczny raport HTML.

**Język generowanego raportu:** Polski

## 2. Business Goal

The application should answer the research question:

> Do empirical data confirm the Solow model prediction that poorer countries tend to grow faster and income differences between countries decrease over time?

The project is intended for students of economics, so the result must be technically correct but also understandable for non-technical readers.

## 3. Functional Requirements

### 3.1 Data Download

The application must automatically download GDP per capita data for selected countries.

Recommended data source:

- World Bank API
- Indicator: `NY.GDP.PCAP.KD`, GDP per capita, constant 2015 US dollars

The script must allow configuration of:

- country list,
- start year,
- end year,
- output directory.

Default country set should include a mixed sample of European economies, for example:

- Poland: `POL`
- Germany: `DEU`
- Czechia: `CZE`
- Slovakia: `SVK`
- Hungary: `HUN`
- Romania: `ROU`
- Bulgaria: `BGR`
- Ukraine: `UKR`
- Spain: `ESP`
- Portugal: `PRT`

Default period: `2000-2023`, unless data availability requires a shorter period.

### 3.2 Data Cleaning

The script must:

- parse downloaded data into a pandas DataFrame,
- normalize country codes, country names, years, and GDP per capita values,
- remove records with missing GDP per capita,
- validate that at least two countries and at least two years are available,
- handle missing data gracefully,
- raise clear user-friendly errors when data cannot be downloaded or processed.

### 3.3 Growth Calculation

The script must calculate average annual GDP per capita growth for every country over the selected period.

Use compound annual growth rate:

```text
CAGR = (GDP_end / GDP_start) ** (1 / number_of_years) - 1
```

The result should include:

- initial GDP per capita,
- final GDP per capita,
- average annual growth rate,
- number of available years.

### 3.4 Beta-Convergence Test

The script must test beta-convergence using a simple cross-sectional regression:

```text
growth_rate = alpha + beta * log(initial_gdp_per_capita) + error
```

Expected interpretation:

- negative beta coefficient means poorer countries grew faster,
- positive beta coefficient means no beta-convergence in the sample,
- p-value should be reported if statsmodels is available.

The output should include:

- beta coefficient,
- intercept,
- R-squared,
- p-value for beta when available,
- plain-English interpretation.

### 3.5 Sigma-Convergence Test

The script must test sigma-convergence by calculating dispersion of log GDP per capita across countries for each year.

Recommended metric:

```text
sigma_t = standard_deviation(log(GDP_per_capita_t))
```

Expected interpretation:

- if sigma decreases from the first year to the last year, income differences decreased,
- if sigma increases, income differences increased.

The output should include:

- sigma value per year,
- first-year sigma,
- last-year sigma,
- percentage change,
- plain-English interpretation.

### 3.6 Charts

The script must generate at least three charts:

1. GDP per capita over time by country.
2. Beta-convergence scatter plot:
   - x-axis: log initial GDP per capita,
   - y-axis: average annual growth rate,
   - regression line.
3. Sigma-convergence chart:
   - x-axis: year,
   - y-axis: standard deviation of log GDP per capita.

Charts should be saved as PNG files in the output directory.

### 3.7 Static Web Report

The script must generate a static HTML report containing:

- project title,
- task description,
- data source and period,
- country list,
- summary table,
- beta-convergence result,
- sigma-convergence result,
- generated charts,
- final conclusions,
- limitations of the analysis.

The report should be saved as:

```text
site/index.html
```

### 3.8 Command-Line Interface

The project should expose a CLI interface.

Example:

```bash
python src/solow_app.py --countries POL DEU CZE SVK HUN ROU BGR UKR ESP PRT --start-year 2000 --end-year 2023 --output-dir site
```

The CLI must support:

- `--countries`
- `--start-year`
- `--end-year`
- `--output-dir`
- `--offline-data` optional local CSV input for tests or offline mode

### 3.9 GitHub Actions Deployment

The repository should include a GitHub Actions workflow that:

- installs Python dependencies,
- runs tests,
- executes the script,
- uploads the generated `site/` folder as GitHub Pages artifact,
- deploys it to GitHub Pages.

Recommended workflow path:

```text
.github/workflows/pages.yml
```

## 4. Non-Functional Requirements

### 4.1 Simplicity

The project must stay lightweight and easy to understand. Avoid heavy frameworks unless necessary.

Preferred stack:

- Python 3.11+
- pandas
- requests
- matplotlib
- statsmodels or scipy
- pytest

No database is required.

### 4.2 Code Quality

The code should be modular and testable.

Recommended structure:

```text
src/
  solow_app.py
  data.py
  analysis.py
  charts.py
  report.py
tests/
  test_data.py
  test_analysis.py
  test_report.py
requirements.txt
Readme.md
Opis.md
```

Comments in code must be simple and written in plain English.

### 4.3 Reliability

The application must:

- work with live World Bank API data,
- work with a local CSV file for tests,
- avoid failing silently,
- provide clear error messages,
- keep generated files deterministic where possible.

### 4.4 Testability

The project must support TDD.

Tests should cover:

- data parsing,
- growth calculation,
- beta-convergence calculation,
- sigma-convergence calculation,
- HTML report generation,
- CLI behavior with offline data.

Network calls should be mocked in unit tests.

### 4.5 Academic Transparency

The report must clearly state that:

- the analysis is simplified,
- GDP per capita is only one economic indicator,
- convergence depends on country sample and period,
- Solow model predictions are theoretical and empirical results may differ.

## 5. Acceptance Criteria

The project is complete when:

1. `pytest` passes locally and in GitHub Actions.
2. The script generates `site/index.html`.
3. At least three PNG charts are generated.
4. The report includes beta-convergence and sigma-convergence interpretation.
5. The repository can be deployed through GitHub Pages.
6. A non-technical student can understand the Polish explanation in `Opis.md`.
