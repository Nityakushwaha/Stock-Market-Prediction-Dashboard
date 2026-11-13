import streamlit as st


def render_kpis(summary: dict) -> None:
    kpis = summary["kpis"]
    sentiment_df = summary["charts"]["sentiment_distribution"]
    total = int(kpis["article_count"])

    positive = 0
    if not sentiment_df.empty:
        row = sentiment_df[sentiment_df["sentiment"] == "Positive"]
        if not row.empty:
            positive = int(row.iloc[0]["count"])

    positive_percent = positive / total * 100 if total else 0
    cards = st.columns(4)

    with cards[0]:
        st.metric("Overall news tone", kpis["overall_sentiment"])
    with cards[1]:
        st.metric("Articles analyzed", total)
    with cards[2]:
        st.metric("Positive headlines", f"{positive_percent:.1f}%")
    with cards[3]:
        st.metric("Average model confidence", f"{kpis['average_confidence']:.1%}")

    st.caption(
        "Confidence describes how certain FinBERT is about article sentiment; it is not a stock-return forecast."
    )
