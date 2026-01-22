# Data Directory Contract

This directory stores all system data with strict lineage rules.

## raw/
- Source: APIs, filings, price feeds
- Immutable (never edited once written)
- Weekly cadence for prices
- Quarterly cadence for fundamentals

## processed/
- Cleaned and normalized data
- Derived only from raw/
- Used by validation and intelligence layers

## snapshots/
- Weekly or quarterly system state
- Includes conviction scores, signals, decisions
- Supports decision journaling and audits

Violating this contract is considered a system error.

