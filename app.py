import streamlit as st

from dashboard.charts import (
    render_sentiment_distribution,
    render_source_distribution,
)
from dashboard.comparison import render_comparison
from dashboard.components import render_kpis
from dashboard.layout import render_empty_state, render_header, render_search
from dashboard.styles import apply_theme
from dashboard.tables import render_articles
from src.core.platform import NewsIntelligencePlatform


@st.cache_resource
def get_platform() -> NewsIntelligencePlatform:
    return NewsIntelligencePlatform()


def main() -> None:
    apply_theme()

    render_header()

    companies, analyze = render_search()

    if not analyze:
        render_empty_state()
        return

    if not companies.strip():
        st.warning("Please enter at least one company.")
        return

    company_list = [
        company.strip() for company in companies.split(",") if company.strip()
    ]

    platform = get_platform()

    progress = st.progress(
        0,
        text="Fetching latest financial news...",
    )

    progress.progress(
        25,
        text="Fetching latest financial news...",
    )

    try:
        with st.spinner("Running analysis..."):
            # -----------------------------
            # Multi-company comparison
            # -----------------------------
            if len(company_list) > 1:
                progress.progress(
                    60,
                    text="Analyzing sentiment with FinBERT...",
                )

                comparison = platform.analyze_many(company_list)

                progress.progress(
                    100,
                    text="Analysis complete!",
                )

                progress.empty()

                render_comparison(comparison["comparison"])

                return

            # -----------------------------
            # Single-company analysis
            # -----------------------------
            progress.progress(
                60,
                text="Analyzing sentiment with FinBERT...",
            )

            result = platform.analyze(company_list[0])

    except ValueError as error:
        progress.empty()
        st.error(str(error))

        st.info(
            """
    ### 💡 Try searching for:

    - **Company names:** Tesla, Apple, Microsoft, NVIDIA
    - **Stock tickers:** TSLA, AAPL, MSFT
    - **Commodities:** Gold, Silver, Crude Oil, Natural Gas
    - **Cryptocurrencies:** Bitcoin, Ethereum
    """
        )

        return

    except RuntimeError as error:
        progress.empty()
        st.error(str(error))
        return

    progress.progress(
        100,
        text="Analysis complete!",
    )

    progress.empty()

    st.subheader(f"News sentiment · {result['company']}")
    st.caption("A summary of the latest relevant articles found by the configured providers.")

    overview_tab, articles_tab, export_tab = st.tabs(
        ["Overview", "Article feed", "Data & export"]
    )

    with overview_tab:
        render_kpis(result["summary"])
        col1, col2 = st.columns(2)
        with col1, st.container(border=True):
            render_sentiment_distribution(
                result["summary"]["charts"]["sentiment_distribution"]
            )
        with col2, st.container(border=True):
            render_source_distribution(
                result["summary"]["charts"]["source_distribution"]
            )
        st.info(
            "Sentiment summarizes the tone of available news; it is not a prediction of future share-price growth."
        )

    with articles_tab:
        render_articles(result["news"])

    with export_tab:
        st.markdown("### Take the results with you")
        st.caption("Download the article-level data used to build this summary.")
        st.dataframe(result["news"], width="stretch", hide_index=True)
        st.download_button(
            label="Download article data (CSV)",
            data=result["news"].to_csv(index=False),
            file_name=f"{company_list[0]}_news_sentiment.csv",
            mime="text/csv",
            type="primary",
        )


if __name__ == "__main__":
    main()
