from __future__ import annotations

from pathlib import Path
import argparse

from src.analysis import calculate_growth, test_beta_convergence, test_sigma_convergence
from src.charts import create_gdp_chart, create_beta_chart, create_sigma_chart
from src.data import fetch_world_bank_data, load_local_csv
from src.report import generate_html_report

DEFAULT_COUNTRIES = ["POL", "DEU", "CZE", "SVK", "HUN", "ROU", "BGR", "UKR", "ESP", "PRT"]


def build_report_context(
    countries: list[str],
    start_year: int,
    end_year: int,
    df,
    growth_df,
    beta_result,
    sigma_df,
    sigma_summary,
    chart_paths: dict[str, Path],
) -> dict[str, object]:
    # Generate research question answer based on beta and sigma results
    beta_value = beta_result.get("beta", 0)
    sigma_change = sigma_summary.get("percentage_change", 0)
    last_sigma = sigma_summary.get("last_sigma", 0)
    first_sigma = sigma_summary.get("first_sigma", 0)
    
    # Build answer to research question
    beta_positive = beta_value < 0
    sigma_decreasing = last_sigma < first_sigma
    
    if beta_positive and sigma_decreasing:
        answer = (
            "Tak, dane empiryczne potwierdzają konwergencję przewidywaną przez model Solowa dla badanej próby krajów. "
            "Zarówno beta-konwergencja, jak i sigma-konwergencja są obserwowane: biedniejsze kraje rosły szybciej, "
            "a różnice dochodowe między krajami zmniejszyły się w badanym okresie. "
            "To sugeruje, że kraje zbliżają się do siebie pod względem dochodów per capita."
        )
    elif beta_positive and not sigma_decreasing:
        answer = (
            "Odpowiedź jest mieszana. Obserwuje się beta-konwergencję (biedniejsze kraje rosły szybciej), "
            "jednak nie obserwuje się sigma-konwergencji (różnice dochodowe nie zmniejszyły się). "
            "Oznacza to, że chociaż biedniejsze kraje doganiają bogatsze w tempie wzrostu, "
            "nierówności dochodowe nie zmniejszyły się w dostatecznym stopniu."
        )
    elif not beta_positive and sigma_decreasing:
        answer = (
            "Odpowiedź jest negatywna. W badanej próbie nie obserwuje się beta-konwergencji. "
            "Chociaż różnice dochodowe między krajami zmniejszyły się, nie jest to wynikiem tego, "
            "że biedniejsze kraje rosły szybciej."
        )
    else:
        answer = (
            "Nie, dane nie potwierdzają przewidywań modelu Solowa dla tej próby. "
            "Biedniejsze kraje nie rosły szybciej niż bogatsze, a różnice dochodowe wzrosły. "
            "To sugeruje brak konwergencji dochodów w badanym okresie."
        )
    
    return {
        "title": "Raport Konwergencji Modelu Solowa",
        "research_question": "Czy dane empiryczne potwierdzają konwergencję przewidywaną przez model Solowa?",
        "research_answer": answer,
        "data_source": "World Bank API / offline CSV",
        "period": f"{start_year} - {end_year}",
        "countries": countries,
        "summary_table": growth_df.to_dict(orient="records"),
        "beta_interpretation": beta_result["interpretation"],
        "sigma_interpretation": sigma_summary["interpretation"],
        "charts": [
            {"title": "Szereg czasowy PKB per capita", "filename": chart_paths["gdp"].name},
            {"title": "Wykres beta-konwergencji", "filename": chart_paths["beta"].name},
            {"title": "Trend sigma-konwergencji", "filename": chart_paths["sigma"].name},
        ],
        "limitations": [
            "Wyniki zależą od wyboru krajów i okresu.",
            "Analiza uwzględnia tylko PKB per capita i nie kontroluje innych czynników.",
            "Raport jest opisowy i nie ustala związków przyczynowych.",
        ],
        "conclusion": answer,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Solow convergence report.")
    parser.add_argument("--countries", nargs="+", default=DEFAULT_COUNTRIES, help="Country codes to include.")
    parser.add_argument("--start-year", type=int, default=2000, help="Start year for the data period.")
    parser.add_argument("--end-year", type=int, default=2023, help="End year for the data period.")
    parser.add_argument("--output-dir", default="site", help="Directory to save report and charts.")
    parser.add_argument("--offline-data", help="Optional local CSV file with country-year GDP per capita data.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.offline_data:
            data_df = load_local_csv(args.offline_data)
        else:
            data_df = fetch_world_bank_data(args.countries, args.start_year, args.end_year)

        growth_df = calculate_growth(data_df)
        beta_result = test_beta_convergence(growth_df)
        sigma_df, sigma_summary = test_sigma_convergence(data_df)

        chart_paths = {
            "gdp": create_gdp_chart(data_df, output_dir),
            "beta": create_beta_chart(growth_df, beta_result, output_dir),
            "sigma": create_sigma_chart(sigma_df, output_dir),
        }

        context = build_report_context(
            countries=args.countries,
            start_year=args.start_year,
            end_year=args.end_year,
            df=data_df,
            growth_df=growth_df,
            beta_result=beta_result,
            sigma_df=sigma_df,
            sigma_summary=sigma_summary,
            chart_paths=chart_paths,
        )

        generate_html_report(context, output_dir)
        print(f"Report generated at: {output_dir / 'index.html'}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
