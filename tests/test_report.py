from pathlib import Path

from src.report import generate_html_report


def test_generate_html_report_creates_file(tmp_path: Path):
    context = {
        "title": "Test Report",
        "research_question": "Does the test work?",
        "data_source": "Test source",
        "period": "2000-2020",
        "countries": ["POL", "DEU"],
        "summary_table": [
            {
                "country_code": "POL",
                "country_name": "Poland",
                "initial_year": 2000,
                "final_year": 2020,
                "initial_gdp_per_capita": 10000.0,
                "final_gdp_per_capita": 20000.0,
                "average_annual_growth": 0.035,
            }
        ],
        "beta_interpretation": "Beta result.",
        "sigma_interpretation": "Sigma result.",
        "charts": [
            {"title": "GDP Chart", "filename": "gdp_per_capita.png"},
            {"title": "Beta Chart", "filename": "beta_convergence.png"},
        ],
        "limitations": ["Limit 1", "Limit 2"],
        "conclusion": "Final conclusion.",
    }

    output_path = generate_html_report(context, tmp_path)
    assert output_path.exists()

    text = output_path.read_text(encoding="utf-8")
    assert "Does the test work?" in text
    assert "Beta result." in text
    assert "Sigma result." in text
    assert "gdp_per_capita.png" in text
    assert "beta_convergence.png" in text
    assert "Limit 1" in text
