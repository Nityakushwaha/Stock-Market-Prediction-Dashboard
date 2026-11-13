import pandas as pd
import plotly.express as px
import streamlit as st

_SENTIMENT = {
    "Positive": "🟢 Positive",
    "Neutral": "⚪ Neutral",
    "Negative": "🔴 Negative",
}


def render_comparison(comparison: list[dict]) -> None:

    st.subheader("Company comparison")
    st.caption(
        "Compare the tone and volume of available news. Confidence refers to FinBERT's sentiment classification."
    )

    if not comparison:
        st.info("No company results were returned.")
        return

    df = pd.DataFrame(comparison)

    df["average_confidence"] = (df["average_confidence"] * 100).round(1)

    df = df.sort_values(
        "average_confidence",
        ascending=False,
    )

    # ---------- KPIs ----------

    top_company = df.iloc[0]

    most_articles = df.loc[df["article_count"].idxmax()]

    mood = df["overall_sentiment"].mode().iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Highest sentiment confidence",
            top_company["company"],
            f"{top_company['average_confidence']:.1f}%",
        )

    with c2:
        st.metric(
            "Most articles found",
            most_articles["company"],
            int(most_articles["article_count"]),
        )

    with c3:
        st.metric(
            "Most common company tone",
            mood,
        )

    st.markdown("### Results by company")

    display = df.copy()

    display["overall_sentiment"] = display["overall_sentiment"].map(_SENTIMENT)

    display = display.rename(
        columns={
            "company": "Company",
            "overall_sentiment": "Sentiment",
            "average_confidence": "Confidence (%)",
            "article_count": "Articles",
        }
    )

    st.dataframe(display, width="stretch", hide_index=True)
    st.download_button(
        label="Download comparison (CSV)",
        data=display.to_csv(index=False),
        file_name="company_comparison.csv",
        mime="text/csv",
    )

    # ---------- Confidence Chart ----------

    st.markdown("### Sentiment model confidence")

    fig = px.bar(
        df,
        x="average_confidence",
        y="company",
        orientation="h",
        text="average_confidence",
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
    )

    fig.update_layout(
        template="plotly_white",
        height=360,
        xaxis_title="Confidence (%)",
        yaxis_title="",
        xaxis={"range": [0, 100]},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={
            "l": 20,
            "r": 20,
            "t": 30,
            "b": 20,
        },
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    # ---------- Sentiment Pie ----------

    st.markdown("### Overall tone across companies")

    sentiment = df["overall_sentiment"].value_counts().reset_index()

    sentiment.columns = [
        "Sentiment",
        "Companies",
    ]

    pie = px.pie(
        sentiment,
        names="Sentiment",
        values="Companies",
        color="Sentiment",
        color_discrete_map={
            "Positive": "#22c55e",
            "Neutral": "#94a3b8",
            "Negative": "#ef4444",
        },
    )

    pie.update_layout(
        height=360,
        margin={
            "l": 20,
            "r": 20,
            "t": 20,
            "b": 20,
        },
    )

    st.plotly_chart(pie, width="stretch", config={"displayModeBar": False})
