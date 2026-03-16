# TRACE MARKETS

TRACE MARKETS is a fundamentals-first decision support system for long-term investing.

It focuses on governance, stability, valuation sanity, and risk-aware conviction.
It is not a trading bot, not a prediction engine, and not an execution platform.

## Current Status

- Phase 1 is complete.
- Deterministic snapshots are generated from file-based inputs.
- Backend API and frontend dashboard are wired and running locally.
- Current local universe is configured to `ITC.NS` in [configs/universe.yaml](configs/universe.yaml).

## Phase-1 Completion (2026-03-16)

Summary of delivered Phase-1 items:

- Deterministic snapshot engine: `tools/build_snapshot.py` and `src/trace_invest/pipeline/snapshot_builder.py` now produce auditable snapshot artifacts in `data/snapshots/YYYY-MM-DD/`.
- Modular analyzers for governance, stability, valuation sanity, and fraud are implemented and integrated into the validation pipeline.
- Conviction scoring and decision zone mapping implemented in `src/trace_invest/intelligence/conviction.py` (deterministic weights).
- Per-stock reasoning stories generated under `reasoning/*.json` (e.g., `ITC_NS.json`).
- FastAPI backend exposes snapshot reads only (no computation in API layer) and serves endpoints under `backend/app/api`.
- Next.js dashboard wired to API and serving market/stock views (`frontend` build verified).
- Added unit tests for analyzers and conviction logic; test suite passes locally.
- TRACE_CODEBASE.md and TRACE_SYSTEM_STATE.md regenerated and pushed.

Operational notes:

- To reproduce Phase-1 outputs: run `f:/Projects/Trace_Finance/.venv/Scripts/python.exe tools/build_snapshot.py` and serve the backend/frontend as described below.
- Artifacts to inspect: `data/snapshots/2026-03-16/snapshot.json`, `market_summary.json`, `metadata.json`, and `reasoning/ITC_NS.json`.

## Phase-2 Roadmap (initial implementation)

Phase-2 introduces continuous market intelligence features (scaffolded and partially implemented):

- Data ingestion stubs: `src/trace_invest/data_ingestion` (local deterministic fetchers and validators).
- Company history builder: `tools/build_history.py` and `src/trace_invest/company_history_engine.py` (writes `data/history/{SYMBOL}.json`). Run `python tools/build_history.py` to regenerate history from snapshots.
- Signal discovery: `src/trace_invest/signal_engine` (rule-based signals and opportunity ranking).
- Portfolio engine: `src/trace_invest/portfolio_engine/engine.py` (deterministic allocations with caps).
- Alerts engine: `src/trace_invest/alerts_engine` (conviction deltas, governance warnings, strong signals).
- Backend Phase-2 API: `/phase2/opportunities`, `/phase2/portfolio`, `/phase2/alerts` (see `backend/app/api/phase2.py`).
- Frontend pages: `/opportunities`, `/alerts`, `/portfolio` (simple initial UI pages wired to API).

CI: basic `pytest` GitHub Actions workflow added at `.github/workflows/ci.yml`.

Next steps: implement external ingestion connectors, expand signals, refine portfolio rules, and add Alert Center UX details.


## What It Does Today

1. Loads stock universe from config.
2. Reads raw fundamentals from local JSON files.
3. Runs validation layers across governance, stability, valuation, and fraud signals.
4. Computes conviction score and decision zone.
5. Compares with previous snapshot and creates delta explanations.
6. Writes snapshot artifacts and per-stock reasoning stories.
7. Serves data through FastAPI.
8. Displays market and stock views in Next.js frontend.

## Architecture

- Backend: FastAPI ([backend/app/main.py](backend/app/main.py))
- Frontend: Next.js App Router ([frontend/app](frontend/app))
- Core pipeline: [src/trace_invest/pipeline/snapshot_builder.py](src/trace_invest/pipeline/snapshot_builder.py)
- Snapshot build command: [tools/build_snapshot.py](tools/build_snapshot.py)
- Configs: [configs](configs)
- Snapshots output: [data/snapshots](data/snapshots)

## Snapshot Outputs

Each run writes:

- `snapshot.json` (full decisions)
- `market_summary.json` (aggregated market stats)
- `metadata.json` (input/config hashes)
- `reasoning/*.json` (stock-level reasoning stories)

Location format:

- `data/snapshots/YYYY-MM-DD/`

## API Endpoints

- `GET /stocks`
- `GET /stocks/{symbol}`
- `GET /stocks/{symbol}/history`
- `GET /stocks/{symbol}/reasoning`
- `GET /market/summary`
- `GET /snapshots`
- `GET /snapshots/{date}/stocks`
- `GET /snapshots/{date}/market`
- `GET /snapshots/snapshots` (latest snapshot payload)

Main API wiring:

- [backend/app/main.py](backend/app/main.py)
- [backend/app/api](backend/app/api)

## Frontend Views

- Dashboard: [frontend/app/dashboard/page.tsx](frontend/app/dashboard/page.tsx)
- Stocks list: [frontend/app/stocks/page.tsx](frontend/app/stocks/page.tsx)
- Stock detail: [frontend/app/stocks/[symbol]/page.tsx](frontend/app/stocks/[symbol]/page.tsx)

## Run Locally

### 1) Build a snapshot (venv)

```bash
cd trace-invest
f:/Projects/Trace_Finance/.venv/Scripts/python.exe tools/build_snapshot.py
```

### 2) Start backend

```bash
cd trace-invest
set PYTHONPATH=F:/Projects/Trace_Finance/trace-invest/src;F:/Projects/Trace_Finance/trace-invest/backend
f:/Projects/Trace_Finance/.venv/Scripts/python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

Docs: `http://127.0.0.1:8000/docs`

### 3) Start frontend

```bash
cd trace-invest/frontend
npm run dev -- --webpack
```

UI: `http://127.0.0.1:3000/dashboard`

## CORS Note

Local development supports both:

- `http://localhost:3000`
- `http://127.0.0.1:3000`

Configured in [backend/app/main.py](backend/app/main.py).

## Scope and Limits

- Deterministic and auditable outputs from local data.
- No real-time ingestion scheduler yet.
- No auth/user system yet.
- No portfolio execution features.
- Phase 2 items (trend overlays, richer exports/alerts) are pending.

## References

- Phase 1 contract: [docs/PHASE1.md](docs/PHASE1.md)
- System inventory snapshot: [TRACE_SYSTEM_STATE.md](TRACE_SYSTEM_STATE.md)
- Codebase notes: [TRACE_CODEBASE.md](TRACE_CODEBASE.md)

