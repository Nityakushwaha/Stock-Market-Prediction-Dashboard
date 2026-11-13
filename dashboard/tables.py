from datetime import datetime, timezone

import humanize
import pandas as pd
import streamlit as st

_BADGE = {
    "Positive": ":green-badge[Positive]",
    "Negative": ":red-badge[Negative]",
    "Neutral": ":gray-badge[Neutral]",
}


def format_relative_time(timestamp: str) -> str:
    if not timestamp:
        return "Time unavailable"
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return humanize.naturaltime(datetime.now(timezone.utc) - dt)


def relevance_badge(score: int) -> str:
    if score >= 20:
        return "⭐⭐⭐ High Relevance"

    if score >= 10:
        return "⭐⭐ Medium Relevance"

    return "⭐ Low Relevance"


def render_articles(df: pd.DataFrame) -> None:
    st.subheader("Recent articles")
    st.caption(f"Showing up to 10 of {len(df)} analyzed articles, ranked by relevance.")

    for _, article in df.head(10).iterrows():

        confidence = article["confidence"] * 100

        badge = _BADGE.get(
            article["sentiment"],
            ":gray-badge[Unknown]",
        )

        description = (
            article.get("description")
            or "No description available."
        )

        with st.container(border=True):

            left, right = st.columns([8, 2])

            with left:

                st.markdown(badge)

                st.markdown(f"**[{article['title']}]({article['url']})**")

                st.caption(
                    f"{article['source']} · {article['provider']} · "
                    f"{format_relative_time(article.get('published_at'))}"
                )

                st.caption(
                    relevance_badge(int(article.get("relevance", 0)))
                )

            with right:

                st.metric(
                    "Sentiment confidence",
                    f"{confidence:.1f}%"
                )

                st.progress(confidence / 100)

            st.write(description)

            st.link_button(
                "Open original article",
                article["url"],
                width="stretch",
            )
