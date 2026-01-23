# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

from trace_invest.config.loader import load_config
from trace_invest.validation.runner import run_validation
from trace_invest.intelligence.conviction import conviction_score
from trace_invest.outputs.signals import generate_signal
from trace_invest.outputs.journal import create_journal_entry

st.set_page_config(
    page_title="Trace Invest Dashboard",
    layout="wide",
)

st.title("Trace Invest — Investing Dashboard")
st.caption("Calm. Explainable. Long-term.")

config = load_config()
stocks = config["universe"]["universe"]["stocks"]

st.header("Watchlist Overview")

rows = []
signals_by_stock = {}

for stock in stocks:
    name = stock["name"]

    processed = {
        "quality_metrics": {
            "roe": 18,
            "debt_to_equity": 0.3,
            "revenue_growth_5y": 12,
            "operating_margin": 18,
        },
        "valuation_metrics": {
            "pe_ratio": 22,
            "pb_ratio": 2.5,
            "fcf_yield": 4.5,
        },
        "financials": {},
        "governance": {},
    }

    validation = run_validation({
        "financials": {},
        "governance": {},
    })

    conviction = conviction_score(processed, validation)
    signal = generate_signal(conviction)

    signals_by_stock[name] = signal

    rows.append({
        "Stock": name,
        "Conviction": conviction["conviction_score"],
        "Zone": signal["zone"],
        "Risk": conviction["overall_risk"],
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True)


st.header("Decision Journal")

selected_stock = st.selectbox(
    "Select a stock",
    [row["Stock"] for row in rows],
)

if selected_stock:
    journal = create_journal_entry(
        selected_stock,
        signals_by_stock[selected_stock],
    )

    st.subheader(f"Decision for {selected_stock}")
    st.json(journal)

