import streamlit as st


def render_header() -> None:
    st.title("📈 Stock Market Prediction Dashboard")
    st.caption(
        "An Explainable Indian Equity Growth Outlook System"
    )
    st.caption(
        "Current prototype: financial-news retrieval and FinBERT sentiment analysis. "
        "Growth outlook, valuation, and risk outputs are still in development."
    )


def render_search() -> tuple[str, bool]:
    with st.container(border=True):
        st.subheader("Analyze company news")
        st.caption(
            "Enter one company, or compare several by separating names with commas."
        )

        with st.form("company_search", clear_on_submit=False):
            company = st.text_input(
                "Company names or tickers",
                placeholder="Infosys, TCS, Reliance, NVIDIA",
                help="Try company names or common stock tickers. Multiple entries are compared side by side.",
            )
            analyze = st.form_submit_button(
                "Analyze news sentiment",
                type="primary",
                width="stretch",
            )

    return company, analyze


def render_empty_state() -> None:
    st.markdown("### Your analysis, at a glance")
    st.caption("A simple three-step view of what this dashboard currently does.")

    steps = st.columns(3)
    descriptions = [
        ("1 · Choose companies", "Search a company or compare several names."),
        ("2 · Analyze recent news", "FinBERT classifies relevant headlines as positive, neutral, or negative."),
        ("3 · Review the evidence", "Explore article-level results, sources, and model confidence."),
    ]
    for column, (title, description) in zip(steps, descriptions):
        with column, st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(description)

    st.info(
        "This version summarizes news sentiment. It does not yet forecast stock returns or provide investment advice."
    )
