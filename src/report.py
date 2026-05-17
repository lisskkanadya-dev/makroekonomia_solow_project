from __future__ import annotations

from pathlib import Path


def generate_html_report(context: dict[str, object], output_dir: Path | str) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "index.html"

    title = context.get("title", "Raport Konwergencji Modelu Solowa")
    research_question = context.get("research_question", "Czy dane empiryczne potwierdzają konwergencję przewidywaną przez model Solowa?")
    research_answer = context.get("research_answer", "")
    data_source = context.get("data_source", "World Bank API")
    period = context.get("period", "")
    countries = context.get("countries", [])
    summary_table = context.get("summary_table", [])
    beta_interpretation = context.get("beta_interpretation", "")
    sigma_interpretation = context.get("sigma_interpretation", "")
    charts = context.get("charts", [])
    limitations = context.get("limitations", [])
    conclusion = context.get("conclusion", "")

    countries_html = ", ".join(countries)
    summary_rows = "".join(
        f"<tr><td>{row['country_code']}</td><td>{row['country_name']}</td>"
        f"<td>{row['initial_year']}</td><td>{row['final_year']}</td>"
        f"<td>{row['initial_gdp_per_capita']:.2f}</td><td>{row['final_gdp_per_capita']:.2f}</td>"
        f"<td>{row['average_annual_growth']:.4f}</td></tr>"
        for row in summary_table
    )
    charts_html = "".join(
        f"<div class='chart'><h3>{chart['title']}</h3>"
        f"<img src='{chart['filename']}' alt='{chart['title']}'></div>"
        for chart in charts
    )
    limitations_html = "".join(f"<li>{item}</li>" for item in limitations)

    html = f"""
<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fb; color: #202124; }}
    .container {{ max-width: 1000px; margin: auto; background: #ffffff; padding: 24px; box-shadow: 0 3px 15px rgba(0,0,0,0.08); }}
    h1, h2, h3 {{ color: #1f2d3d; }}
    table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
    th, td {{ border: 1px solid #d1d5db; padding: 10px; text-align: left; }}
    th {{ background: #f1f5f9; }}
    .chart {{ margin: 24px 0; }}
    img {{ max-width: 100%; border: 1px solid #d1d5db; }}
    ul {{ margin: 0; padding-left: 20px; }}
    .answer-box {{ background: #e8f4f8; padding: 16px; border-left: 4px solid #0288d1; margin: 16px 0; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{title}</h1>
    <p><strong>Pytanie badawcze:</strong> {research_question}</p>
    <div class="answer-box">
      <p><strong>Odpowiedź na pytanie badawcze:</strong></p>
      <p>{research_answer}</p>
    </div>
    <p><strong>Źródło danych:</strong> {data_source}</p>
    <p><strong>Okres:</strong> {period}</p>
    <p><strong>Kraje:</strong> {countries_html}</p>
    <h2>Podsumowanie</h2>
    <table>
      <thead>
        <tr>
          <th>Kod</th>
          <th>Kraj</th>
          <th>Rok początkowy</th>
          <th>Rok końcowy</th>
          <th>PKB początkowy</th>
          <th>PKB końcowy</th>
          <th>Wzrost roczny</th>
        </tr>
      </thead>
      <tbody>
        {summary_rows}
      </tbody>
    </table>
    <h2>Beta-konwergencja</h2>
    <p>{beta_interpretation}</p>
    <h2>Sigma-konwergencja</h2>
    <p>{sigma_interpretation}</p>
    {charts_html}
    <h2>Wnioski</h2>
    <p>{conclusion}</p>
    <h2>Ograniczenia</h2>
    <ul>
      {limitations_html}
    </ul>
  </div>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")
    return path
