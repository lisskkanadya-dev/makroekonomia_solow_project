# Prompt for GitHub Copilot: Generate Automated Tests for Solow Convergence Project

<role>
You are GitHub Copilot working as a senior Python QA engineer and TDD specialist.
Your task is to generate automated tests before the implementation is written.
</role>

<context>
The project is a lightweight Python web application for an academic economics assignment.
It downloads GDP per capita data, calculates average annual growth, tests beta-convergence and sigma-convergence, generates charts, and creates a static HTML report for GitHub Pages.
</context>

<main_goal>
Generate a complete pytest test suite that defines the expected behavior of the future Python implementation.
The tests should guide development using a TDD approach.
</main_goal>

<expected_project_structure>
Assume this structure:

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
  test_cli.py
requirements.txt
Readme.md
Opis.md
</expected_project_structure>

<technical_stack>
Use:
- Python 3.11+
- pytest
- pandas
- numpy
- requests-mock or monkeypatch for network mocking
- pathlib
- tempfile or tmp_path pytest fixture
</technical_stack>

<testing_rules>
1. Do not call the real World Bank API in unit tests.
2. Use small deterministic sample datasets.
3. Tests must be readable and easy to maintain.
4. Test names must describe business behavior.
5. Prefer exact assertions for deterministic calculations.
6. Use approximate assertions for floating point values.
7. Do not test implementation details that are not part of expected behavior.
8. Include tests for error handling.
9. Include tests for CLI execution in offline mode.
10. Keep comments simple and in plain English.
</testing_rules>

<sample_dataset>
Use a small artificial dataset similar to this:

country_code,country_name,year,gdp_per_capita
POL,Poland,2000,10000
POL,Poland,2020,20000
DEU,Germany,2000,40000
DEU,Germany,2020,50000
ROU,Romania,2000,5000
ROU,Romania,2020,18000

This dataset should show beta-convergence because poorer countries grow faster.
</sample_dataset>

<required_tests>
Generate tests for the following behavior.

<data_tests>
File: tests/test_data.py

Test cases:
1. Local CSV data is loaded into a pandas DataFrame.
2. Required columns are validated.
3. Missing GDP values are removed.
4. A clear ValueError is raised when fewer than two countries are available.
5. A clear ValueError is raised when fewer than two years are available.
6. World Bank API JSON is parsed into normalized columns:
   - country_code
   - country_name
   - year
   - gdp_per_capita
7. Network errors are converted into a clear RuntimeError.
</data_tests>

<analysis_tests>
File: tests/test_analysis.py

Test cases:
1. CAGR is calculated correctly for every country.
2. Initial and final GDP values are selected from the first and last available year.
3. Beta-convergence returns a negative beta for the sample dataset.
4. Beta-convergence output includes beta, intercept, r_squared, and interpretation.
5. Sigma-convergence calculates dispersion for every year.
6. Sigma-convergence detects decreasing dispersion when final sigma is lower than initial sigma.
7. Analysis handles missing middle years without crashing.
8. Analysis raises ValueError when GDP values are zero or negative before logarithmic calculations.
</analysis_tests>

<report_tests>
File: tests/test_report.py

Test cases:
1. HTML report file is created in the output directory.
2. HTML report contains the research question.
3. HTML report contains beta-convergence interpretation.
4. HTML report contains sigma-convergence interpretation.
5. HTML report references all generated chart files.
6. HTML report contains limitations section.
</report_tests>

<chart_tests>
File: tests/test_charts.py

Test cases:
1. GDP time-series chart file is created.
2. Beta-convergence scatter chart file is created.
3. Sigma-convergence chart file is created.
4. Chart functions return paths to generated PNG files.
</chart_tests>

<cli_tests>
File: tests/test_cli.py

Test cases:
1. CLI runs successfully with --offline-data.
2. CLI creates index.html in output directory.
3. CLI creates expected PNG files.
4. CLI exits with non-zero status for invalid input data.
</cli_tests>
</required_tests>

<expected_public_api>
Assume these functions will exist. Write tests against them:

from src.data import load_local_csv, fetch_world_bank_data, validate_dataset
from src.analysis import calculate_growth, test_beta_convergence, test_sigma_convergence
from src.charts import create_gdp_chart, create_beta_chart, create_sigma_chart
from src.report import generate_html_report

Expected function behavior:
- load_local_csv(path) -> pandas.DataFrame
- fetch_world_bank_data(countries, start_year, end_year) -> pandas.DataFrame
- validate_dataset(df) -> pandas.DataFrame
- calculate_growth(df) -> pandas.DataFrame
- test_beta_convergence(growth_df) -> dict
- test_sigma_convergence(df) -> pandas.DataFrame, dict
- create_gdp_chart(df, output_dir) -> pathlib.Path
- create_beta_chart(growth_df, beta_result, output_dir) -> pathlib.Path
- create_sigma_chart(sigma_df, output_dir) -> pathlib.Path
- generate_html_report(context, output_dir) -> pathlib.Path
</expected_public_api>

<output_format>
Create test files with complete executable pytest code.
Also generate any required pytest fixtures.
Use pathlib.Path and tmp_path where possible.
</output_format>

<quality_bar>
The generated tests should be strong enough that a developer can implement the full project from them.
Avoid vague placeholder tests.
</quality_bar>
