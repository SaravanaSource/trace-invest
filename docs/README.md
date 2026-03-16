# TRACE MARKETS — Documentation

This folder is the canonical documentation for TRACE MARKETS. It consolidates
the project README and long-lived reference docs so the team has a single
authoritative place to look for system status, quickstarts, and architecture
notes.

---

Consolidated from `trace-invest/README.md` — last updated 2026-03-16.

# TRACE MARKETS

TRACE MARKETS is a fundamentals-first, auditable decision-support system for
long-term investing. It focuses on governance, stability, valuation sanity,
and risk-aware conviction. The project is research-first and designed to be
reproducible and explainable; it is not a live execution platform (yet).

## Current Status (Summary)

- Phase-1..Phase-3 core components implemented (snapshot engine, analyzers,
  factor research, backtesting scaffolding).
- Phase-4 (Alpha Factory) implemented: deterministic signal discovery, strategy
  generator, ranking, monitoring, alpha scoring, orchestration script, and
  FastAPI endpoints under `/alpha/*`.
- Phase-5 (Platform scaffolding) implemented: lightweight auth stubs, user
  profiles, portfolio endpoints, market connector stub, insight generator,
  notification & monitoring stubs.
- Frontend: Next.js Alpha Lab UI pages added under `/alpha-lab` (production
  build verified). Demo data and deterministic backtests included for
  reproducible demos.

## What’s included (Phase‑4 / Phase‑5)

- Alpha Factory (`src/trace_invest/alpha_factory/`)
  - `signal_lab`: rule-based signal discovery that writes
    `src/data/signals/signals.json`.
  - `strategy_generator`: composes deterministic candidate strategies and
    writes `src/data/generated_strategies/`.
  - `backtests` placeholders: deterministic backtest artifacts under
    `src/data/backtests/` (replaceable with real backtester).
  - `strategy_ranking`: computes alpha scores and writes
    `src/data/strategy_rankings/strategy_rankings.json`.
  - `strategy_monitor`: monitoring artifacts under
    `src/data/strategy_monitoring/`.
- API additions: `backend/app/api/alpha.py` exposes `/alpha/signals`,
  `/alpha/strategies`, `/alpha/rankings`, `/alpha/monitoring`, `/alpha/top`.
- Frontend Alpha Lab: `frontend/app/alpha-lab/*` pages that call the alpha APIs.
- Platform scaffolding: auth (`src/trace_invest/api/auth.py`), portfolios,
  insight engine, notification & monitoring skeletons.

## Quickstart — Alpha Lab demo

1) Ensure virtualenv is active and `PYTHONPATH` includes `src`.

2) Recreate demo artifacts (deterministic demo history and backtests are
included):

```powershell
Set-Location trace-invest
$env:PYTHONPATH='src'
& .venv/Scripts/python.exe tools/run_alpha_factory.py
```

This runs discovery → strategy generation → (placeholder) backtests →
ranking → monitoring and writes artifacts under `src/data/`.

3) Start the backend (FastAPI) — default port 8000:

```powershell
Set-Location trace-invest
$env:PYTHONPATH='src;backend'
& .venv/Scripts/python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

4) Start the frontend (production preview served by Next.js):

```powershell
Set-Location trace-invest/frontend
npm run build
npx next start -p 3001
```

Alpha Lab UI: `http://localhost:3001/alpha-lab` (the pages call the backend
`/alpha/*` endpoints on port 8000).

## Data paths (current)

- Demo and runtime artifacts are written to `src/data/` (signals,
  generated_strategies, backtests, strategy_rankings, strategy_monitoring,
  insights).
- Market connector stub writes `data/market_prices.json` at repo root.
  Recommendation: consolidate to a single canonical data root (we suggest
  `src/data/`).

## Recommended next steps

- Consolidate `data/` vs `src/data/` paths so backend & frontend read the
  same canonical artifacts.
- Replace backtest placeholders with the real backtester in
  `src/trace_invest/research/backtesting_engine/` and wire it into
  `tools/run_alpha_factory.py`.
- Add docker-compose with Postgres/Redis/Celery for background jobs and
  multi-user persistence.

## API Endpoints (high level)

- Snapshot & market: `/stocks`, `/stocks/{symbol}`, `/market/summary`,
  `/snapshots` (existing)
- Research / Alpha: `/alpha/signals`, `/alpha/strategies`, `/alpha/rankings`,
  `/alpha/monitoring` (new)
- Auth & portfolio: `/auth/*`, `/portfolio/*` (scaffolded)

## Run locally (summary commands)

```powershell
# run snapshot / history builds
Set-Location trace-invest
$env:PYTHONPATH='src'
& .venv/Scripts/python.exe tools/build_snapshot.py

# run Alpha Factory pipeline (discovery → strategies → rank → monitor)
& .venv/Scripts/python.exe tools/run_alpha_factory.py

# start backend
$env:PYTHONPATH='src;backend'
& .venv/Scripts/python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

# start frontend (production preview)
Set-Location trace-invest/frontend
npm run build
npx next start -p 3001
```

## Notes

- The system is intentionally deterministic for auditability — deterministic
  heuristics and hash-based placeholders are used for demo backtests.
- If you want, I can (A) consolidate data paths and re-run the pipeline, (B)
  wire the real backtester into the pipeline, or (C) scaffold Docker + Postgres
  now.

## References

- See `tools/run_alpha_factory.py`, `src/trace_invest/alpha_factory/*`, and
  `backend/app/api/alpha.py` for the Alpha Factory implementation.
- Demo artifacts: `src/data/` (signals, generated_strategies, backtests,
  rankings, monitoring, insights).

---

Last update: 2026-03-16 — Phase-4/Phase-5 additions and Alpha Lab demo.

