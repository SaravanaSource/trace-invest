# TRACE MARKETS

TRACE MARKETS is a fundamentals-first decision support system for long-term investing.

It focuses on governance, stability, valuation sanity, and risk-aware conviction.
It is not a trading bot, not a prediction engine, and not an execution platform.

## Current Status

- Phase 1 is complete.
- Deterministic snapshots are generated from file-based inputs.
- Backend API and frontend dashboard are wired and running locally.
- Current local universe is configured to `ITC.NS` in [configs/universe.yaml](configs/universe.yaml).

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

