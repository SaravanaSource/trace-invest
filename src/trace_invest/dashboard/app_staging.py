import streamlit as st

# -------------------------------
# STAGING IDENTITY (VERY IMPORTANT)
# -------------------------------
st.set_page_config(
    page_title="TRACE MARKETS — STAGING",
    layout="wide",
)

st.title("TRACE MARKETS — STAGING")
st.caption("⚠️ Experimental environment. Not for users.")

# -------------------------------
# LOAD PROD APP LOGIC
# -------------------------------
from app import *  # noqa

st.subheader("Data Quality")


q = processed.get("quality", {})
st.metric("Confidence", q.get("confidence", "N/A"))
st.write("Coverage:", q.get("coverage"))
st.write("Freshness:", q.get("freshness"))


