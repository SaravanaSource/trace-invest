import streamlit as st

st.set_page_config(
    page_title="TRACE MARKETS — STAGING",
    layout="wide",
)

st.title("TRACE MARKETS — STAGING")
st.caption("⚠️ Experimental environment. Not for users.")

# IMPORTANT:
# Staging must NOT access internal variables like `processed`
# It only calls the main app runner.

from app import run_app

run_app()
