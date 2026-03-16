# Trace Invest Phase 1

**PHASE 1 STATUS: ✅ COMPLETE**

## Goals
Phase 1 formalizes snapshot generation and makes every output deterministic,
repeatable, and auditable.

## End-to-end flow
1. Read configs from configs/.
2. Load universe from configs/universe.yaml (stocks list or stocks_file).
3. Load raw fundamentals from data/raw/fundamentals (no external calls).
4. Compute processed fundamentals and quality confidence.
5. Run validation to produce governance, stability, master bands.
6. Compute conviction score and decision zone.
7. Generate narrative text and delta explanations.
8. Write snapshot.json, market_summary.json, metadata.json to
   data/snapshots/YYYY-MM-DD/.

## Snapshot schema v1 (core fields)
- schema_version
- run_date
- run_timestamp
- decisions[]
  - stock
  - symbol
  - timestamp
  - decision_zone
  - conviction_score
  - overall_risk
  - master { master_score, master_band }
  - governance { governance_score, governance_band, top_risks }
  - stability { stability_score, stability_band, weak_areas }
  - valuation { valuation_sanity }
  - quality { confidence_band }
  - narrative
  - trend { trend, delta }
  - delta { from_previous, changes, change_summary }
  - validation (full validation payload for audit)

## Market summary v1
- total_stocks
- by_decision_zone
- by_overall_risk
- upgrades / downgrades
- risk_increases / risk_decreases
- band_shifts (master/governance/stability/valuation)
- market_tone (rule-based)

## Run command
- python tools/build_snapshot.py --date YYYY-MM-DD
- If --date is omitted, today in configs/system.yaml timezone is used.

## Phase 2 TODO (do not implement)
- Add price-based trend and momentum inputs.
- Add snapshot-to-snapshot diff export (CSV or markdown).
- Expand market summary with sector-level breakdowns.
- Add validation coverage metrics to dashboard API.
- Add alert outputs for new HIGH risk entries.

## Phase 1 guarantees
- Deterministic snapshots from file-based inputs.
- Delta-aware explanations for what changed between snapshots.
- Market-level aggregation and tone for dashboards.
- Frontend-aligned schema that matches UI expectations.

**Frontend is now fully wired to Phase 1 outputs.**

## What Phase 1 is NOT
- No ML or predictive logic.
- No trading signals or execution logic.
- No database or real-time ingestion.
- No authentication or personalization.

## Phase 2 preview (no implementation)
- Add price trend and momentum overlays.
- Add snapshot diff exports for audit packs.
- Add sector and watchlist rollups.
