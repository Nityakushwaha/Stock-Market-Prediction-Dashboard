import os

from dotenv import load_dotenv

try:
    import streamlit as st
    from streamlit.errors import StreamlitSecretNotFoundError
except ImportError:
    st = None
    StreamlitSecretNotFoundError = Exception

load_dotenv()


def get_secret(key: str) -> str:
    """Retrieve a secret from Streamlit or the environment."""

    if st is not None:
        try:
            return st.secrets[key]
        except (KeyError, StreamlitSecretNotFoundError):
            pass

    return os.getenv(key, "")


MARKETAUX_API_KEY = get_secret("MARKETAUX_API_KEY")
NEWS_API_KEY = get_secret("NEWS_API_KEY")
FINNHUB_API_KEY = get_secret("FINNHUB_API_KEY")
HF_TOKEN = get_secret("HF_TOKEN")