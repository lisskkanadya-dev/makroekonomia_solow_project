# Prompt for GitHub Copilot: Generate Python Code for Solow Convergence Project

<role>
You are GitHub Copilot working as a senior Python developer and business analyst.
You must implement a lightweight, testable Python project for an academic economics assignment.
</role>

<context>
The project tests empirical predictions of the Solow growth model using GDP per capita data.
It should be simple enough for students, but structured enough for software development.
It will be deployed through GitHub Actions to GitHub Pages as a static web report.
</context>

<main_goal>
Implement a Python application that:
1. downloads or loads GDP per capita data,
2. calculates average annual growth,
3. tests beta-convergence,
4. tests sigma-convergence,
5. generates charts,
6. creates a static HTML report in Polish language.
</main_goal>

<project_structure>
Create or update these files:

src/
  __init__.py
  solow_app.py
  data.py
  analysis.py
  charts.py
  report.py
tests/
requirements.txt
.github/workflows/pages.yml
Readme.md
Opis.md
</project_structure>

<technology>
Use:
- Python 3.11+
- pandas
- numpy
- requests
- matplotlib
- statsmodels if available, otherwise numpy/scipy fallback
- pytest for tests

Do not use Flask, Django, FastAPI, or a database.
The final output must be static HTML and PNG files.
</technology>

<coding_style>
1. Write clear modular functions.
2. Keep comments simple and in plain English.
3. Use type hints where helpful.
4. Use pathlib.Path for file paths.
5. Use argparse for CLI.
6. Raise clear ValueError or RuntimeError exceptions.
7. Avoid hidden global state.
8. Keep functions small and testable.
</coding_style>

<data_source>
Use World Bank API.
Indicator:
NY.GDP.PCAP.KD
Meaning:
GDP per capita, constant 2015 US dollars.

World Bank API URL pattern:
https://api.worldbank.org/v2/country/{country_codes}/indicator/NY.GDP.PCAP.KD?format=json&per_page=20000

The country code list should be semicolon-separated for the API.
</data_source>

<default_configuration>
Default countries:
POL DEU CZE SVK HUN ROU BGR UKR ESP PRT

Default start year:
2000

Default end year:
2023

Default output directory:
site
</default_configuration>

<required_public_api>
Implement these functions:

from src.data:
- load_local_csv(path) -> pandas.DataFrame
- fetch_world_bank_data(countries, start_year, end_year) -> pandas.DataFrame
- validate_dataset(df) -> pandas.DataFrame

from src.analysis:
- calculate_growth(df) -> pandas.DataFrame
- test_beta_convergence(growth_df) -> dict
- test_sigma_convergence(df) -> tuple[pandas.DataFrame, dict]

from src.charts:
- create_gdp_chart(df, output_dir) -> pathlib.Path
- create_beta_chart(growth_df, beta_result, output_dir) -> pathlib.Path
- create_sigma_chart(sigma_df, output_dir) -> pathlib.Path

from src.report:
- generate_html_report(context, output_dir) -> pathlib.Path
</required_public_api>

<implementation_details>
<data_module>
load_local_csv:
- read CSV from a path,
- return a normalized pandas DataFrame,
- call validate_dataset before returning.

fetch_world_bank_data:
- call World Bank API with requests,
- parse JSON,
- keep records between start_year and end_year,
- normalize columns:
  country_code, country_name, year, gdp_per_capita,
- call validate_dataset before returning,
- convert network problems into RuntimeError with a clear message.

validate_dataset:
- require columns: country_code, country_name, year, gdp_per_capita,
- convert year to int,
- convert gdp_per_capita to float,
- drop rows with missing GDP,
- reject zero or negative GDP values,
- require at least two countries,
- require at least two years.
</data_module>

<analysis_module>
calculate_growth:
- for each country, sort by year,
- use first available GDP and last available GDP,
- calculate CAGR,
- return columns:
  country_code, country_name, initial_year, final_year, initial_gdp_per_capita, final_gdp_per_capita, average_annual_growth, available_years.

Beta-convergence:
- x = log(initial_gdp_per_capita),
- y = average_annual_growth,
- estimate linear regression,
- return dict with beta, intercept, r_squared, p_value, interpretation.
- interpretation should clearly say whether beta-convergence is observed.

Sigma-convergence:
- for each year, calculate standard deviation of log GDP per capita across countries,
- return sigma_df and summary dict,
- summary includes first_year, last_year, first_sigma, last_sigma, percentage_change, interpretation.
</analysis_module>

<charts_module>
Use matplotlib.
Each chart must be saved as PNG.
Do not require a display server. Use Agg backend.

Required charts:
1. gdp_per_capita.png
2. beta_convergence.png
3. sigma_convergence.png
</charts_module>

<report_module>
Generate static HTML.
The HTML report must include:
- title,
- task description,
- research question,
- data source,
- country list,
- period,
- summary table,
- beta-convergence interpretation,
- sigma-convergence interpretation,
- charts,
- limitations,
- final conclusion.

Use simple CSS embedded in the HTML.
Do not depend on external assets except generated PNG files.
</report_module>

<cli_module>
Create src/solow_app.py with argparse.
Supported arguments:
- --countries, nargs="+"
- --start-year, int
- --end-year, int
- --output-dir
- --offline-data

Behavior:
- if --offline-data is provided, load CSV instead of calling API,
- otherwise call World Bank API,
- run full analysis pipeline,
- generate charts,
- generate index.html,
- print final output path.
</cli_module>
</implementation_details>

<github_actions>
Create .github/workflows/pages.yml.
Workflow should:
1. run on push to main and workflow_dispatch,
2. checkout repository,
3. set up Python 3.11,
4. install requirements,
5. run pytest,
6. run python -m src.solow_app,
7. upload site folder as GitHub Pages artifact,
8. deploy to GitHub Pages.
</github_actions>

<readme_requirements>
Readme.md must be in English and aimed at programmers.
It should include:
- project purpose,
- installation,
- local run command,
- offline run command,
- test command,
- deployment notes,
- project structure.

Opis.md must be in Polish and aimed at economics students.
It should include:
- original task description,
- explanation of Solow model idea,
- explanation of beta-convergence,
- explanation of sigma-convergence,
- how to read the generated charts,
- how to interpret results,
- limitations.
</readme_requirements>

<quality_bar>
The implementation must pass the tests generated from Prompt_tests.md.
The project must be simple, transparent, and suitable for academic demonstration.
Do not over-engineer.
</quality_bar>
