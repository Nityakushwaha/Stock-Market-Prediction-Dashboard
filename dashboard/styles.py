import streamlit as st


def apply_theme() -> None:
    st.set_page_config(
        page_title="Stock Market Prediction Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(
        """
<style>

.block-container {
    max-width: 1480px;
    padding-top: 2.25rem;
    padding-bottom: 3rem;
    padding-left: 2.25rem;
    padding-right: 2.25rem;
}

h1 {
    font-weight: 750;
    letter-spacing: -0.04em;
    color: #0f172a;
}

h2, h3 {
    letter-spacing: -0.02em;
}

section[data-testid="stSidebar"] {
    display: none;
}

div[data-testid="stTextInput"] input {
    border-radius: 10px;
    min-height: 2.8rem;
}

div[data-testid="stButton"] button,
div[data-testid="stFormSubmitButton"] button {
    border-radius: 10px;
    min-height: 2.8rem;
    font-weight: 600;
}

div[data-testid="stMetric"] {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 0.9rem 1rem;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""",
        unsafe_allow_html=True,
    )
