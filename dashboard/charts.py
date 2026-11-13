import pandas as pd
import plotly.graph_objects as go
import streamlit as st

POSITIVE = "#22c55e"
NEGATIVE = "#ef4444"
NEUTRAL = "#94a3b8"


def render_sentiment_distribution(df: pd.DataFrame) -> None:
    colors = [
        {"Positive": POSITIVE, "Negative": NEGATIVE}.get(sentiment, NEUTRAL)
        for sentiment in df["sentiment"]
    ]

    fig = go.Figure()

    fig.add_bar(
        x=df["sentiment"],
        y=df["count"],
        text=df["count"],
        textposition="outside",
        marker_color=colors,
    )

    fig.update_layout(
        title="Article sentiment",
        template="plotly_white",
        height=360,
        margin={
            "l": 20,
            "r": 20,
            "t": 55,
            "b": 20,
        },
        showlegend=False,
        xaxis_title="",
        yaxis_title="Number of articles",
        font={"family": "Arial, sans-serif", "color": "#334155"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False},
    )


def render_source_distribution(df: pd.DataFrame) -> None:

    data = df.head(8).sort_values("count")

    fig = go.Figure()

    fig.add_bar(
        x=data["count"],
        y=data["source"],
        orientation="h",
        marker_color="#2563eb",
        text=data["count"],
        textposition="outside",
    )

    fig.update_layout(
        title="Where the news came from",
        template="plotly_white",
        height=360,
        margin={
            "l": 20,
            "r": 20,
            "t": 60,
            "b": 20,
        },
        showlegend=False,
        xaxis_title="Articles",
        yaxis_title="",
        font={"family": "Arial, sans-serif", "color": "#334155"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False},
    )
