# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

from trace_invest.config.loader import load_config
from trace_invest.validation.runner import run_validation
from trace_invest.intelligence.conviction import conviction_score
from trace_invest.outputs.signals import generate_signal
from trace_invest.outputs.journal import create_journal_entry
from trace_invest.dashboard.snapshots import list_snapshots, load_snapshot


# ------------------------------------------------------------------------------
# Page setup
# ------------------------------------------------------------------------------

st.set_page_config(
    page_title="Trace Invest Dashboard",
    layout="wide",
)

st.title("Trace Invest — Investing Dashboard")
st.caption("Calm. Explainable. Long-term.")

# ------------------------------------------------------------------------------
# Load config
# ------------------------------------------------------------------------------

config = load_config()
stocks = config["universe"]["universe"]["stocks"]

# ------------------------------------------------------------------------------
# Compute system outputs (NO UI HERE)
# ------------------------------------------------------------------------------

rows = []
signals_by_stock = {}
journals_by_stock = {}

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

    validation = run_validation(
        {
            "financials": {},
            "governance": {},
        }
    )

    conviction = conviction_score(processed, validation)
    signal = generate_signal(conviction)
    journal = create_journal_entry(name, signal)

    signals_by_stock[name] = signal
    journals_by_stock[name] = journal

    rows.append(
        {
            "Stock": name,
            "Conviction": conviction["conviction_score"],
            "Zone": signal["zone"],
            "Risk": conviction["overall_risk"],
        }
    )

df = pd.DataFrame(rows)

# ------------------------------------------------------------------------------
# Watchlist Overview
# ------------------------------------------------------------------------------

st.header("Watchlist Overview")
st.dataframe(df, use_container_width=True)

# ------------------------------------------------------------------------------
# Decision Journal
# ------------------------------------------------------------------------------

st.header("Decision Journal")

selected_stock = st.selectbox(
    "Select a stock",
    df["Stock"].tolist(),
    key="current_stock_selector",
)

journal = journals_by_stock[selected_stock]

st.subheader(f"Decision for {selected_stock}")
st.json(journal)

# ------------------------------------------------------------------------------
# Snapshot Viewer
# ------------------------------------------------------------------------------

st.divider()
st.header("Snapshot Viewer")

snapshots = list_snapshots()

if not snapshots:
    st.info("No snapshots found yet. Run the weekly pipeline first.")
else:
    snapshot_names = [p.name for p in snapshots]

    selected_snapshot_name = st.selectbox(
        "Select a weekly snapshot",
        snapshot_names,
        key="snapshot_selector",
    )

    snapshot_path = next(p for p in snapshots if p.name == selected_snapshot_name)
    snapshot = load_snapshot(snapshot_path)

    st.caption(f"Run timestamp: {snapshot['run_timestamp']}")

    decisions = snapshot["decisions"]

    st.subheader("Decisions in this snapshot")
    st.dataframe(decisions, use_container_width=True)

    st.subheader("Inspect a decision")

    snapshot_stocks = [d["stock"] for d in decisions]

    selected_snapshot_stock = st.selectbox(
        "Select stock from snapshot",
        snapshot_stocks,
        key="snapshot_stock_selector",
    )

    decision = next(d for d in decisions if d["stock"] == selected_snapshot_stock)
    st.json(decision)
