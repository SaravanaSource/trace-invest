# TRACE CODEBASE SNAPSHOT

## PROJECT TREE
README.md
backend/__init__.py
backend/app/__init__.py
backend/app/api/__init__.py
backend/app/api/market.py
backend/app/api/snapshots.py
backend/app/api/stocks.py
backend/app/main.py
backend/app/services/snapshot_loader.py
configs/_deprecated_markets.yaml
configs/data_sources.yaml
configs/risk.yaml
configs/system.yaml
configs/universe.yaml
docker-compose.yml
docs/PHASE1.md
docs/README.md
frontend/app/dashboard/page.tsx
frontend/app/globals.css
frontend/app/layout.tsx
frontend/app/page.tsx
frontend/app/stocks/[symbol]/page.tsx
frontend/app/stocks/[symbol]/reasoning/page.tsx
frontend/app/stocks/page.tsx
frontend/components/ui/Card.tsx
frontend/components/ui/Stat.tsx
frontend/lib/api.ts
frontend/next.config.ts
frontend/package-lock.json
frontend/package.json
frontend/tailwind.config.js
frontend/tsconfig.json
pyproject.toml
src/trace_invest/__init__.py
src/trace_invest/api/history.py
src/trace_invest/config/__init__.py
src/trace_invest/config/loader.py
src/trace_invest/dashboard/app.py
src/trace_invest/dashboard/app_staging.py
src/trace_invest/dashboard/snapshots.py
src/trace_invest/governance/balance_sheet_stress.py
src/trace_invest/governance/capital_allocation.py
src/trace_invest/governance/earnings_quality.py
src/trace_invest/governance/governance_score.py
src/trace_invest/governance/promoter_pledge.py
src/trace_invest/governance/tax_volatility.py
src/trace_invest/governance/unusual_items.py
src/trace_invest/ingestion/__init__.py
src/trace_invest/ingestion/fundamentals.py
src/trace_invest/ingestion/prices.py
src/trace_invest/intelligence/__init__.py
src/trace_invest/intelligence/conviction.py
src/trace_invest/intelligence/master_score.py
src/trace_invest/intelligence/quality.py
src/trace_invest/intelligence/valuation.py
src/trace_invest/memory/reader.py
src/trace_invest/outputs/__init__.py
src/trace_invest/outputs/history.py
src/trace_invest/outputs/journal.py
src/trace_invest/outputs/narrative.py
src/trace_invest/outputs/rankings.py
src/trace_invest/outputs/sector_trends.py
src/trace_invest/outputs/sectors.py
src/trace_invest/outputs/signals.py
src/trace_invest/outputs/trends.py
src/trace_invest/outputs/watchlist.py
src/trace_invest/pipeline/__init__.py
src/trace_invest/pipeline/delta.py
src/trace_invest/pipeline/market_summary.py
src/trace_invest/pipeline/reasoning_story.py
src/trace_invest/pipeline/snapshot_builder.py
src/trace_invest/portfolio/engine.py
src/trace_invest/portfolio/exit_manager.py
src/trace_invest/portfolio/mutate.py
src/trace_invest/portfolio/rebalance.py
src/trace_invest/portfolio/store.py
src/trace_invest/portfolio/valuation.py
src/trace_invest/processing/fundamentals.py
src/trace_invest/quality/confidence.py
src/trace_invest/quality/coverage.py
src/trace_invest/quality/freshness.py
src/trace_invest/quality/raw_field_inventory.py
src/trace_invest/quality/raw_profiler.py
src/trace_invest/quality/raw_schema.py
src/trace_invest/run_weekly.py
src/trace_invest/stability/consistency.py
src/trace_invest/stability/fcf_cagr.py
src/trace_invest/stability/median_operating_margin.py
src/trace_invest/stability/median_roe.py
src/trace_invest/stability/registry.py
src/trace_invest/stability/revenue_cagr.py
src/trace_invest/stability/stability_score.py
src/trace_invest/stability/stability_taxonomy.py
src/trace_invest/technical/entry_filter.py
src/trace_invest/technical/momentum.py
src/trace_invest/technical/score.py
src/trace_invest/technical/trend.py
src/trace_invest/utils/__init__.py
src/trace_invest/utils/logger.py
src/trace_invest/validation/__init__.py
src/trace_invest/validation/data_confidence.py
src/trace_invest/validation/fraud.py
src/trace_invest/validation/governance.py
src/trace_invest/validation/governance_score.py
src/trace_invest/validation/registry.py
src/trace_invest/validation/runner.py
src/trace_invest/validation/system_awareness.py
src/trace_invest/valuation/registry.py
src/trace_invest/valuation/sanity.py
tools/build_snapshot.py
tools/md_to_project.py
tools/project_to_md.py
tools/system_state_to_md.py

---

### FILE: README.md
```md
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


```

### FILE: backend/__init__.py
```py

```

### FILE: backend/app/__init__.py
```py

```

### FILE: backend/app/api/__init__.py
```py

```

### FILE: backend/app/api/market.py
```py
from fastapi import APIRouter, HTTPException
from app.services.snapshot_loader import load_latest_market_summary

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/summary")
def get_market_summary():
    try:
        return load_latest_market_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

```

### FILE: backend/app/api/snapshots.py
```py
from fastapi import APIRouter, HTTPException
from app.services.snapshot_loader import (
    list_snapshot_dates,
    load_snapshot_by_date,
    load_market_summary_by_date
)

router = APIRouter(prefix="/snapshots", tags=["snapshots"])


@router.get("")
def get_snapshot_dates():
    return list_snapshot_dates()


@router.get("/{date}/stocks")
def get_snapshot_stocks(date: str):
    try:
        snapshot = load_snapshot_by_date(date)
        return snapshot["decisions"]
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{date}/market")
def get_snapshot_market(date: str):
    try:
        return load_market_summary_by_date(date)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/snapshots")
def get_latest_snapshot():
    dates = list_snapshot_dates()
    if not dates:
        raise HTTPException(status_code=404, detail="No snapshots found")

    latest = sorted(dates)[-1]
    snapshot = load_snapshot_by_date(latest)
    return snapshot


```

### FILE: backend/app/api/stocks.py
```py
from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from app.services.snapshot_loader import (
    load_latest_snapshot,
    load_latest_reasoning_story,
)


def _safe_get(obj, key, default=None):
    """Safely get nested dict values, return None if not found."""
    if obj is None or not isinstance(obj, dict):
        return default
    return obj.get(key, default)


def _build_stock_response(stock_obj):
    return {
        "stock": stock_obj.get("stock"),
        "timestamp": stock_obj.get("timestamp"),
        "decision_zone": stock_obj.get("decision_zone"),
        "overall_risk": stock_obj.get("overall_risk"),
        "conviction_score": stock_obj.get("conviction_score"),
        "narrative": stock_obj.get("narrative"),
        "master": stock_obj.get("master"),
        "governance": stock_obj.get("governance"),
        "stability": stock_obj.get("stability"),
        "valuation": stock_obj.get("valuation"),
        "trend": stock_obj.get("trend"),
        "quality": stock_obj.get("quality"),
    }


router = APIRouter(prefix="/stocks", tags=["stocks"])

BASE_DIR = Path(__file__).resolve().parents[3]
HISTORY_DIR = BASE_DIR / "data" / "history"


@router.get("")
def get_stocks():
    try:
        snapshot = load_latest_snapshot()
        decisions = snapshot["decisions"]
        return [_build_stock_response(stock) for stock in decisions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}")
def get_stock(symbol: str):
    try:
        snapshot = load_latest_snapshot()
        decisions = snapshot["decisions"]
        symbol = symbol.upper()

        for stock_obj in decisions:
            if stock_obj.get("stock", "").upper() == symbol:
                return _build_stock_response(stock_obj)

        raise HTTPException(status_code=404, detail="Stock not found")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/history")
def get_stock_history(symbol: str):
    symbol = symbol.upper()
    path = HISTORY_DIR / f"{symbol}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="History not found")

    try:
        data = json.loads(path.read_text())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    rows = []
    for row in data:
        rows.append({
            "date": row.get("date"),
            "master_band": row.get("master_band"),
            "decision_zone": row.get("decision_zone"),
            "governance_band": row.get("governance_band"),
            "stability_band": row.get("stability_band"),
            "valuation_sanity": row.get("valuation_sanity"),
            "overall_risk": row.get("overall_risk"),
            "trend": row.get("trend"),
        })

    rows.sort(key=lambda r: r.get("date") or "", reverse=True)
    return rows


@router.get("/{symbol}/reasoning")
def get_stock_reasoning(symbol: str):
    try:
        return load_latest_reasoning_story(symbol)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

```

### FILE: backend/app/main.py
```py
from fastapi import FastAPI
from pathlib import Path
import sys
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from backend.app.api.stocks import router as stocks_router
from backend.app.api.market import router as market_router
from backend.app.api.snapshots import router as snapshots_router
from trace_invest.api.history import router as history_router

app = FastAPI(title="Trace Markets API")

# CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks_router)
app.include_router(market_router)
app.include_router(snapshots_router)
app.include_router(history_router)

```

### FILE: backend/app/services/snapshot_loader.py
```py
import json
import math
from pathlib import Path

# In Docker, data is mounted at /app/data
# In local dev, it's at the project root
BASE_DIR = Path(__file__).resolve().parents[3]
if (BASE_DIR / "data" / "snapshots").exists():
    SNAPSHOT_ROOT = BASE_DIR / "data" / "snapshots"
elif Path("/app/data/snapshots").exists():
    SNAPSHOT_ROOT = Path("/app/data/snapshots")
else:
    SNAPSHOT_ROOT = Path("data/snapshots")



def _sanitize(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


def list_snapshot_dates():
    if not SNAPSHOT_ROOT.exists():
        return []

    return sorted([d.name for d in SNAPSHOT_ROOT.iterdir() if d.is_dir()])


def load_snapshot_by_date(date: str):
    path = SNAPSHOT_ROOT / date / "snapshot.json"
    if not path.exists():
        raise FileNotFoundError("Snapshot not found")
    with open(path, "r", encoding="utf-8") as f:
        return _sanitize(json.load(f))


def load_market_summary_by_date(date: str):
    path = SNAPSHOT_ROOT / date / "market_summary.json"
    if not path.exists():
        raise FileNotFoundError("Market summary not found")
    with open(path, "r", encoding="utf-8") as f:
        return _sanitize(json.load(f))


def load_latest_snapshot():
    dates = list_snapshot_dates()
    if not dates:
        raise FileNotFoundError("No snapshots found")
    snapshot = load_snapshot_by_date(dates[-1])
    print("FULL SNAPSHOT KEYS:", snapshot.keys())
    decisions = snapshot.get("decisions", [])
    itc_snapshot = None
    for d in decisions:
        if isinstance(d, dict) and d.get("stock") == "ITC":
            itc_snapshot = d
            break
    print("ITC SNAPSHOT:", itc_snapshot)
    return snapshot


def load_latest_market_summary():
    dates = list_snapshot_dates()
    if not dates:
        raise FileNotFoundError("No snapshots found")
    return load_market_summary_by_date(dates[-1])


def load_latest_reasoning_story(symbol: str):
    dates = list_snapshot_dates()
    if not dates:
        raise FileNotFoundError("No snapshots found")
    return load_reasoning_story_by_date(symbol, dates[-1])


def load_reasoning_story_by_date(symbol: str, date: str):
    snapshot = load_snapshot_by_date(date)
    decision = _find_decision(snapshot, symbol)
    if not decision:
        raise FileNotFoundError("Stock not found in snapshot")

    filename = _reasoning_filename(decision)
    path = SNAPSHOT_ROOT / date / "reasoning" / filename
    if not path.exists():
        raise FileNotFoundError("Reasoning story not found")

    with open(path, "r", encoding="utf-8") as f:
        return _sanitize(json.load(f))


def _find_decision(snapshot: dict, symbol: str):
    decisions = snapshot.get("decisions", [])
    target = symbol.strip().upper()

    for decision in decisions:
        stock = str(decision.get("stock") or "").upper()
        sym = str(decision.get("symbol") or "").upper()
        if stock == target or sym == target:
            return decision
    return None


def _reasoning_filename(decision: dict) -> str:
    symbol = decision.get("symbol")
    if symbol:
        base = str(symbol).replace(".", "_")
    else:
        base = str(decision.get("stock") or "UNKNOWN").replace(" ", "_")

    cleaned = "".join(ch for ch in base.upper() if ch.isalnum() or ch == "_")
    return f"{cleaned}.json"

```

### FILE: configs/_deprecated_markets.yaml
```yaml
markets:
  commodities:
    enabled: true
    instruments:
      - gold
      - silver
      - copper
      - aluminium
      - uranium

  equities:
    enabled: false

  forex:
    enabled: false


```

### FILE: configs/data_sources.yaml
```yaml
data_sources:
  prices:
    cadence: weekly
    source: primary

  fundamentals:
    cadence: quarterly
    source: filings

  news:
    enabled: true
    governance_focus: true


```

### FILE: configs/risk.yaml
```yaml
risk:
  max_capital_per_trade_pct: 5.0
  max_single_stock_allocation_pct: 20.0
  drawdown_alert_pct: 15.0


```

### FILE: configs/system.yaml
```yaml
environment: dev

logging:
  level: INFO
  file: trace-invest.log

timezone: Asia/Kolkata

data_dir: data/


```

### FILE: configs/universe.yaml
```yaml
universe:
  stocks:
    - name: ITC
      symbol: ITC.NS
    # - name: HDFC Bank
    #   symbol: HDFCBANK.NS
    # - name: TCS
    #   symbol: TCS.NS
    # - name: Larsen & Toubro
    #   symbol: LT.NS
    # - name: Asian Paints
    #   symbol: ASIANPAINT.NS

  stocks_file: data/universe/nifty50.json



cadence:
  prices: weekly
  fundamentals: quarterly


```

### FILE: docker-compose.yml
```yml
version: "3.9"

services:
  api:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data:ro
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_BASE_URL: http://localhost:8000
    depends_on:
      - api
    restart: unless-stopped


```

### FILE: docs/PHASE1.md
```md
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

```

### FILE: docs/README.md
```md
# Trace Invest — Documentation

This folder contains long-lived, authoritative documents.

## Tracker
- `Trace_Invest_Tracker_v2.pdf`
  - Canonical system status
  - Architecture lock
  - Vision lock
  - Long-term reference (10+ years)

If there is ever a conflict between code and tracker,
**the tracker wins**.


```

### FILE: frontend/app/dashboard/page.tsx
```tsx
import { Card } from "@/components/ui/Card";
import { Stat } from "@/components/ui/Stat";
import { getMarketSummary } from "@/lib/api";

type MarketSummary = {
  total_stocks: number;
  by_decision_zone: Record<string, number>;
  by_overall_risk: Record<string, number>;
  upgrades?: number;
  downgrades?: number;
  market_tone?: string;
};

function formatMap(map: Record<string, number> | undefined) {
  if (!map || Object.keys(map).length === 0) {
    return <div className="text-white/60">No data</div>;
  }

  return (
    <ul className="space-y-1 text-white/80">
      {Object.entries(map).map(([key, value]) => (
        <li key={key} className="flex items-center justify-between">
          <span>{key}</span>
          <span className="font-semibold text-white">{value}</span>
        </li>
      ))}
    </ul>
  );
}

export default async function Dashboard() {
  let summary: MarketSummary | null = null;

  try {
    summary = await getMarketSummary();
  } catch (error) {
    console.error(error);
  }

  if (!summary) {
    return <div className="p-6 text-white/60">Failed to load market summary.</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      <div className="grid gap-4 md:grid-cols-4">
        <Stat label="Total Stocks" value={summary.total_stocks} />
        <Stat label="Upgrades" value={summary.upgrades ?? 0} tone="good" />
        <Stat label="Downgrades" value={summary.downgrades ?? 0} tone="bad" />
        <Stat label="Market Tone" value={summary.market_tone || "UNKNOWN"} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <div className="text-sm text-white/60 mb-3">Decision Zones</div>
          {formatMap(summary.by_decision_zone)}
        </Card>
        <Card>
          <div className="text-sm text-white/60 mb-3">Risk Bands</div>
          {formatMap(summary.by_overall_risk)}
        </Card>
      </div>
    </div>
  );
}

```

### FILE: frontend/app/globals.css
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  background: #020617;
  color: #e5e7eb;
}

```

### FILE: frontend/app/layout.tsx
```tsx
import "./globals.css";
import Link from "next/link";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex min-h-screen">
        {/* Sidebar */}
        <aside className="w-60 bg-panel border-r border-border p-6">
          <h1 className="text-xl font-bold mb-8">TRACE MARKETS</h1>

          <nav className="space-y-4 text-muted">
            <Link href="/dashboard" className="block hover:text-text">
              Dashboard
            </Link>
            <Link href="/stocks" className="block hover:text-text">
              Stocks
            </Link>
          </nav>
        </aside>

        {/* Content */}
        <main className="flex-1 p-10">{children}</main>
      </body>
    </html>
  );
}

```

### FILE: frontend/app/page.tsx
```tsx
import Image from "next/image";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={100}
          height={20}
          priority
        />
        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            To get started, edit the page.tsx file.
          </h1>
          <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            Looking for a starting point or more instructions? Head over to{" "}
            <a
              href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
              className="font-medium text-zinc-950 dark:text-zinc-50"
            >
              Templates
            </a>{" "}
            or the{" "}
            <a
              href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
              className="font-medium text-zinc-950 dark:text-zinc-50"
            >
              Learning
            </a>{" "}
            center.
          </p>
        </div>
        <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
          <a
            className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
            href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={16}
              height={16}
            />
            Deploy Now
          </a>
          <a
            className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-black/[.08] px-5 transition-colors hover:border-transparent hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] md:w-[158px]"
            href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            Documentation
          </a>
        </div>
      </main>
    </div>
  );
}

```

### FILE: frontend/app/stocks/[symbol]/page.tsx
```tsx
"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card } from "@/components/ui/Card";
import { getLatestSnapshot } from "@/lib/api";

type StockData = any;

type NarrativeView = {
  summary: string;
  details: string[];
};

function buildSystemView(data: StockData) {
  const reasons: string[] = [];

  if (data.stability?.stability_band) {
    reasons.push(`Stability is ${data.stability.stability_band}`);
  }

  if (data.valuation?.valuation_sanity) {
    reasons.push(`Valuation is ${data.valuation.valuation_sanity}`);
  }

  if (data.overall_risk) {
    reasons.push(`Overall risk is ${data.overall_risk}`);
  }

  return {
    decision: data.decision_zone,
    masterBand: data.master?.master_band,
    masterScore: data.master?.master_score,
    confidence: data.quality?.confidence_band,
    reasons,
  };
}

function normalizeNarrative(narrative: any): NarrativeView {
  if (!narrative) {
    return { summary: "No narrative available", details: [] };
  }

  if (typeof narrative === "string") {
    return { summary: narrative, details: [] };
  }

  const summary = narrative.summary || "No narrative available";
  const details: string[] = Array.isArray(narrative.details)
    ? narrative.details
    : narrative.details
    ? [String(narrative.details)]
    : [];

  return { summary, details };
}

function formatBandChanges(bandChanges: Record<string, string> | undefined) {
  if (!bandChanges) {
    return [];
  }

  const labelMap: Record<string, string> = {
    valuation: "Valuation",
    stability: "Stability",
    governance: "Governance",
  };

  return Object.entries(labelMap)
    .filter(([key]) => bandChanges[key])
    .map(([key, label]) => `${label} ${bandChanges[key].toLowerCase()}`);
}

export default function StockDetailPage() {
  const params = useParams();
  const symbol = params.symbol as string;

  const [data, setData] = useState<StockData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLatestSnapshot()
      .then((res) => {
        const decisions = Array.isArray(res?.decisions) ? res.decisions : [];
        const match = decisions.find((decision: any) => {
          const stock = String(decision?.stock || "").toUpperCase();
          const sym = String(decision?.symbol || "").toUpperCase();
          const requested = String(symbol || "").toUpperCase();
          return stock === requested || sym === requested;
        });

        setData(match || null);
      })
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [symbol]);

  if (loading) {
    return <div className="p-6 text-white/60">Loading...</div>;
  }

  if (!data) {
    return <div className="p-6 text-white/60">No data available</div>;
  }

  const systemView = buildSystemView(data);
  const narrative = normalizeNarrative(data.narrative);
  const delta = data.delta || {};
  const bandChanges = formatBandChanges(delta.band_changes);

  return (
    <div className="p-6 space-y-6 text-white">
      <div>
        <h1 className="text-2xl font-bold">{symbol}</h1>
        <div className="text-sm text-white/60">
          Snapshot at {data.timestamp}
        </div>
      </div>

      <Card>
        <h2 className="text-lg font-semibold mb-2">Narrative</h2>
        <p className="text-white/80">{narrative.summary}</p>
        {narrative.details.length > 0 && (
          <details className="mt-3 text-white/70">
            <summary className="cursor-pointer">Narrative details</summary>
            <ul className="list-disc pl-5 mt-2 space-y-1">
              {narrative.details.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </details>
        )}
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-2">
          What Changed Since Last Snapshot
        </h2>
        <p className="text-white/80">
          {delta.change_summary || "No change summary available"}
        </p>
        <div className="mt-3 space-y-1 text-white/70">
          {delta.decision_change && delta.decision_change !== "UNCHANGED" && (
            <div>Decision: {delta.decision_change}</div>
          )}
          {delta.risk_change && delta.risk_change !== "UNCHANGED" && (
            <div>Risk: {delta.risk_change}</div>
          )}
          {bandChanges.map((change, index) => (
            <div key={index}>{change}</div>
          ))}
        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-3">System View</h2>
        <div className="mb-2">
          This stock is in{" "}
          <span className="font-semibold">{systemView.decision}</span> zone
          because:
        </div>

        <ul className="list-disc pl-5 text-white/70 space-y-1">
          {systemView.reasons.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>

        <div className="mt-4 text-white/70">
          Master Band:{" "}
          <span className="font-semibold">
            {systemView.masterBand} ({systemView.masterScore})
          </span>
        </div>

        <div className="text-white/70">
          Confidence Level:{" "}
          <span className="font-semibold">
            {systemView.confidence || "UNKNOWN"}
          </span>
        </div>
      </Card>
    </div>
  );
}

```

### FILE: frontend/app/stocks/[symbol]/reasoning/page.tsx
```tsx
import { Card } from "@/components/ui/Card";
import { getStockReasoning } from "@/lib/api";

function renderFacts(title: string, facts: any[]) {
  if (!facts || facts.length === 0) {
    return <div className="text-white/60">No data</div>;
  }

  return (
    <div className="space-y-2">
      <div className="text-sm text-white/60">{title}</div>
      <ul className="space-y-2">
        {facts.map((fact, index) => (
          <li key={index} className="border border-white/10 rounded-lg p-3">
            <div className="font-semibold text-white">{fact.name}</div>
            <div className="text-sm text-white/70">
              Status: {fact.status || "UNKNOWN"} | Risk: {fact.risk || "UNKNOWN"}
            </div>
            {fact.explanation && (
              <div className="text-sm text-white/70 mt-1">
                {fact.explanation}
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default async function ReasoningStoryPage({
  params,
}: {
  params: { symbol: string };
}) {
  const story = await getStockReasoning(params.symbol);

  const metadata = story.metadata || {};
  const facts = story.observed_facts || {};
  const rules = story.interpretation_rules || [];
  const aggregation = story.aggregation_logic || {};
  const delta = story.delta_interpretation || {};
  const verdict = story.final_verdict || {};
  const guidance = story.verification_guidance || [];

  return (
    <div className="p-6 space-y-6 text-white">
      <div>
        <h1 className="text-2xl font-bold">Reasoning Story</h1>
        <div className="text-sm text-white/60">
          {metadata.stock} ({metadata.symbol}) — {metadata.run_date}
        </div>
      </div>

      <Card>
        <h2 className="text-lg font-semibold mb-2">1. What was evaluated</h2>
        <div className="text-white/70">
          {(story.evaluation_scope?.categories || []).join(", ") ||
            "No scope available"}
        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">2. What was observed</h2>
        <div className="space-y-4">
          {renderFacts("Governance", facts.governance)}
          {renderFacts("Stability", facts.stability)}
          {renderFacts("Valuation", facts.valuation)}
          {renderFacts("Fraud", facts.fraud)}
          {renderFacts("Other", facts.other)}
        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">3. How it was interpreted</h2>
        <ul className="space-y-3 text-white/80">
          {rules.map((rule: any, index: number) => (
            <li key={index} className="border border-white/10 rounded-lg p-3">
              <div className="font-semibold">{rule.statement}</div>
              <div className="text-sm text-white/70 mt-1">
                Inputs: {JSON.stringify(rule.inputs || {})}
              </div>
              <div className="text-sm text-white/70">
                Result: {JSON.stringify(rule.result || {})}
              </div>
            </li>
          ))}
        </ul>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">4. Aggregation logic</h2>
        <pre className="text-sm text-white/70 whitespace-pre-wrap">
          {JSON.stringify(aggregation, null, 2)}
        </pre>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">5. What changed</h2>
        <div className="text-white/80">
          {delta.change_summary || "No change summary available"}
        </div>
        {Array.isArray(delta.changes) && delta.changes.length > 0 && (
          <ul className="list-disc pl-5 mt-2 text-white/70 space-y-1">
            {delta.changes.map((change: string, index: number) => (
              <li key={index}>{change}</li>
            ))}
          </ul>
        )}
        {delta.verdict_impact && (
          <div className="text-white/70 mt-2">
            Verdict impact: {delta.verdict_impact}
          </div>
        )}
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">6. Final verdict</h2>
        <div className="text-white/80">
          Decision zone: {verdict.decision_zone || "UNKNOWN"}
        </div>
        <div className="text-white/80">
          Overall risk: {verdict.overall_risk || "UNKNOWN"}
        </div>
        {Array.isArray(verdict.primary_reasons) && (
          <ul className="list-disc pl-5 mt-2 text-white/70 space-y-1">
            {verdict.primary_reasons.map((reason: string, index: number) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
        )}
        {Array.isArray(verdict.uncertainties) && verdict.uncertainties.length > 0 && (
          <div className="mt-3 text-white/70">
            Uncertainties: {verdict.uncertainties.join(", ")}
          </div>
        )}
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">7. How to verify</h2>
        <ul className="list-disc pl-5 text-white/70 space-y-1">
          {guidance.map((item: string, index: number) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Card>
    </div>
  );
}

```

### FILE: frontend/app/stocks/page.tsx
```tsx
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getLatestSnapshot } from "@/lib/api";

type Stock = {
  stock: string;
  decision_zone: string;
  conviction_score: number;
  overall_risk: string;
  delta?: {
    decision_change?: string;
  };
};

export default function StocksPage() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLatestSnapshot()
      .then((res) => {
        if (Array.isArray(res?.decisions)) {
          setStocks(res.decisions);
        } else {
          console.error("Unexpected snapshot response:", res);
          setStocks([]);
        }
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to load stocks");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="p-6 text-white/60">Loading stocks…</div>;
  }

  if (error) {
    return <div className="p-6 text-red-400">{error}</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Stocks</h1>

      <table className="w-full border-collapse">
        <thead>
          <tr className="text-left text-white/60 border-b border-white/10">
            <th className="py-2">Stock</th>
            <th className="py-2">Decision</th>
            <th className="py-2">Conviction</th>
            <th className="py-2">Risk</th>
          </tr>
        </thead>

        <tbody>
          {stocks.map((s) => (
            <Link
              key={s.stock || "unknown"}
              href={`/stocks/${encodeURIComponent(s.stock || "UNKNOWN")}`}
              className="contents"
            >
              <tr className="border-b border-white/5 hover:bg-white/5 cursor-pointer transition">
                <td className="py-2">{s.stock}</td>
                <td className="py-2">
                  <div className="flex items-center gap-2">
                    <span>{s.decision_zone}</span>
                    {s.delta?.decision_change === "UPGRADE" && (
                      <span className="text-xs uppercase border border-white/10 text-white/70 rounded px-2 py-0.5">
                        Upgraded
                      </span>
                    )}
                    {s.delta?.decision_change === "DOWNGRADE" && (
                      <span className="text-xs uppercase border border-white/10 text-white/70 rounded px-2 py-0.5">
                        Downgraded
                      </span>
                    )}
                  </div>
                </td>
                <td className="py-2">{s.conviction_score}</td>
                <td className="py-2">{s.overall_risk}</td>
              </tr>
            </Link>
          ))}
        </tbody>
      </table>
    </div>
  );
}

```

### FILE: frontend/components/ui/Card.tsx
```tsx
export function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-panel border border-border rounded-xl p-6">
      {children}
    </div>
  );
}


```

### FILE: frontend/components/ui/Stat.tsx
```tsx
export function Stat({
  label,
  value,
  tone = "default",
}: {
  label: string;
  value: string | number;
  tone?: "good" | "warn" | "bad" | "default";
}) {
  const tones: any = {
    good: "text-good",
    warn: "text-warn",
    bad: "text-bad",
    default: "text-text",
  };

  return (
    <div className="bg-panel border border-border rounded-xl p-6">
      <p className="text-muted text-sm">{label}</p>
      <p className={`text-3xl font-semibold mt-1 ${tones[tone]}`}>
        {value}
      </p>
    </div>
  );
}


```

### FILE: frontend/lib/api.ts
```ts
const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export async function getStocks() {
  const res = await fetch(`${API_BASE}/stocks`);

  if (!res.ok) {
    const text = await res.text();
    console.error("API /stocks failed:", res.status, text);
    throw new Error("Failed to fetch stocks");
  }

  return res.json();
}

export async function getMarketSummary() {
  const res = await fetch(`${API_BASE}/market/summary`);

  if (!res.ok) {
    const text = await res.text();
    console.error("API /market/summary failed:", res.status, text);
    throw new Error("Failed to fetch market summary");
  }

  return res.json();
}

export async function getLatestSnapshot() {
  const res = await fetch(`${API_BASE}/snapshots/snapshots`);

  if (!res.ok) {
    const text = await res.text();
    console.error("API /snapshots/snapshots failed:", res.status, text);
    throw new Error("Failed to fetch latest snapshot");
  }

  return res.json();
}

export async function getStockReasoning(symbol: string) {
  const res = await fetch(`${API_BASE}/stocks/${symbol}/reasoning`);

  if (!res.ok) {
    const text = await res.text();
    console.error("API /stocks/{symbol}/reasoning failed:", res.status, text);
    throw new Error("Failed to fetch reasoning story");
  }

  return res.json();
}

```

### FILE: frontend/next.config.ts
```ts
const nextConfig = {
  images: { unoptimized: true },
};

```

### FILE: frontend/package-lock.json
```json
{
  "name": "frontend",
  "version": "0.1.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "frontend",
      "version": "0.1.0",
      "dependencies": {
        "next": "16.1.6",
        "react": "19.2.3",
        "react-dom": "19.2.3"
      },
      "devDependencies": {
        "@types/node": "^20",
        "@types/react": "^19",
        "@types/react-dom": "^19",
        "autoprefixer": "^10.4.23",
        "eslint": "^9",
        "eslint-config-next": "16.1.6",
        "postcss": "^8.5.6",
        "tailwindcss": "^3.4.1",
        "typescript": "^5"
      }
    },
    "node_modules/@alloc/quick-lru": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/@alloc/quick-lru/-/quick-lru-5.2.0.tgz",
      "integrity": "sha512-UrcABB+4bUrFABwbluTIBErXwvbsU/V7TZWfmbgJfbkwiBuziS9gxdODUyuiecfdGQ85jglMW6juS3+z5TsKLw==",
      "dev": true,
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/@babel/code-frame": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/code-frame/-/code-frame-7.28.6.tgz",
      "integrity": "sha512-JYgintcMjRiCvS8mMECzaEn+m3PfoQiyqukOMCCVQtoJGYJw8j/8LBJEiqkHLkfwCcs74E3pbAUFNg7d9VNJ+Q==",
      "dev": true,
      "dependencies": {
        "@babel/helper-validator-identifier": "^7.28.5",
        "js-tokens": "^4.0.0",
        "picocolors": "^1.1.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/compat-data": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/compat-data/-/compat-data-7.28.6.tgz",
      "integrity": "sha512-2lfu57JtzctfIrcGMz992hyLlByuzgIk58+hhGCxjKZ3rWI82NnVLjXcaTqkI2NvlcvOskZaiZ5kjUALo3Lpxg==",
      "dev": true,
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/core": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/core/-/core-7.28.6.tgz",
      "integrity": "sha512-H3mcG6ZDLTlYfaSNi0iOKkigqMFvkTKlGUYlD8GW7nNOYRrevuA46iTypPyv+06V3fEmvvazfntkBU34L0azAw==",
      "dev": true,
      "dependencies": {
        "@babel/code-frame": "^7.28.6",
        "@babel/generator": "^7.28.6",
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-module-transforms": "^7.28.6",
        "@babel/helpers": "^7.28.6",
        "@babel/parser": "^7.28.6",
        "@babel/template": "^7.28.6",
        "@babel/traverse": "^7.28.6",
        "@babel/types": "^7.28.6",
        "@jridgewell/remapping": "^2.3.5",
        "convert-source-map": "^2.0.0",
        "debug": "^4.1.0",
        "gensync": "^1.0.0-beta.2",
        "json5": "^2.2.3",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/babel"
      }
    },
    "node_modules/@babel/generator": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/generator/-/generator-7.28.6.tgz",
      "integrity": "sha512-lOoVRwADj8hjf7al89tvQ2a1lf53Z+7tiXMgpZJL3maQPDxh0DgLMN62B2MKUOFcoodBHLMbDM6WAbKgNy5Suw==",
      "dev": true,
      "dependencies": {
        "@babel/parser": "^7.28.6",
        "@babel/types": "^7.28.6",
        "@jridgewell/gen-mapping": "^0.3.12",
        "@jridgewell/trace-mapping": "^0.3.28",
        "jsesc": "^3.0.2"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-compilation-targets": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-compilation-targets/-/helper-compilation-targets-7.28.6.tgz",
      "integrity": "sha512-JYtls3hqi15fcx5GaSNL7SCTJ2MNmjrkHXg4FSpOA/grxK8KwyZ5bubHsCq8FXCkua6xhuaaBit+3b7+VZRfcA==",
      "dev": true,
      "dependencies": {
        "@babel/compat-data": "^7.28.6",
        "@babel/helper-validator-option": "^7.27.1",
        "browserslist": "^4.24.0",
        "lru-cache": "^5.1.1",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-globals": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/helper-globals/-/helper-globals-7.28.0.tgz",
      "integrity": "sha512-+W6cISkXFa1jXsDEdYA8HeevQT/FULhxzR99pxphltZcVaugps53THCeiWA8SguxxpSp3gKPiuYfSWopkLQ4hw==",
      "dev": true,
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-imports": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-imports/-/helper-module-imports-7.28.6.tgz",
      "integrity": "sha512-l5XkZK7r7wa9LucGw9LwZyyCUscb4x37JWTPz7swwFE/0FMQAGpiWUZn8u9DzkSBWEcK25jmvubfpw2dnAMdbw==",
      "dev": true,
      "dependencies": {
        "@babel/traverse": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-transforms": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-transforms/-/helper-module-transforms-7.28.6.tgz",
      "integrity": "sha512-67oXFAYr2cDLDVGLXTEABjdBJZ6drElUSI7WKp70NrpyISso3plG9SAGEF6y7zbha/wOzUByWWTJvEDVNIUGcA==",
      "dev": true,
      "dependencies": {
        "@babel/helper-module-imports": "^7.28.6",
        "@babel/helper-validator-identifier": "^7.28.5",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-string-parser": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-string-parser/-/helper-string-parser-7.27.1.tgz",
      "integrity": "sha512-qMlSxKbpRlAridDExk92nSobyDdpPijUq2DW6oDnUqd0iOGxmQjyqhMIihI9+zv4LPyZdRje2cavWPbCbWm3eA==",
      "dev": true,
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-identifier": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-identifier/-/helper-validator-identifier-7.28.5.tgz",
      "integrity": "sha512-qSs4ifwzKJSV39ucNjsvc6WVHs6b7S03sOh2OcHF9UHfVPqWWALUsNUVzhSBiItjRZoLHx7nIarVjqKVusUZ1Q==",
      "dev": true,
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-option": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-option/-/helper-validator-option-7.27.1.tgz",
      "integrity": "sha512-YvjJow9FxbhFFKDSuFnVCe2WxXk1zWc22fFePVNEaWJEu8IrZVlda6N0uHwzZrUM1il7NC9Mlp4MaJYbYd9JSg==",
      "dev": true,
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helpers": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helpers/-/helpers-7.28.6.tgz",
      "integrity": "sha512-xOBvwq86HHdB7WUDTfKfT/Vuxh7gElQ+Sfti2Cy6yIWNW05P8iUslOVcZ4/sKbE+/jQaukQAdz/gf3724kYdqw==",
      "dev": true,
      "dependencies": {
        "@babel/template": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/parser": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/parser/-/parser-7.28.6.tgz",
      "integrity": "sha512-TeR9zWR18BvbfPmGbLampPMW+uW1NZnJlRuuHso8i87QZNq2JRF9i6RgxRqtEq+wQGsS19NNTWr2duhnE49mfQ==",
      "dev": true,
      "dependencies": {
        "@babel/types": "^7.28.6"
      },
      "bin": {
        "parser": "bin/babel-parser.js"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@babel/template": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/template/-/template-7.28.6.tgz",
      "integrity": "sha512-YA6Ma2KsCdGb+WC6UpBVFJGXL58MDA6oyONbjyF/+5sBgxY/dwkhLogbMT2GXXyU84/IhRw/2D1Os1B/giz+BQ==",
      "dev": true,
      "dependencies": {
        "@babel/code-frame": "^7.28.6",
        "@babel/parser": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/traverse": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/traverse/-/traverse-7.28.6.tgz",
      "integrity": "sha512-fgWX62k02qtjqdSNTAGxmKYY/7FSL9WAS1o2Hu5+I5m9T0yxZzr4cnrfXQ/MX0rIifthCSs6FKTlzYbJcPtMNg==",
      "dev": true,
      "dependencies": {
        "@babel/code-frame": "^7.28.6",
        "@babel/generator": "^7.28.6",
        "@babel/helper-globals": "^7.28.0",
        "@babel/parser": "^7.28.6",
        "@babel/template": "^7.28.6",
        "@babel/types": "^7.28.6",
        "debug": "^4.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/types": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/types/-/types-7.28.6.tgz",
      "integrity": "sha512-0ZrskXVEHSWIqZM/sQZ4EV3jZJXRkio/WCxaqKZP1g//CEWEPSfeZFcms4XeKBCHU0ZKnIkdJeU/kF+eRp5lBg==",
      "dev": true,
      "dependencies": {
        "@babel/helper-string-parser": "^7.27.1",
        "@babel/helper-validator-identifier": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@emnapi/core": {
      "version": "1.8.1",
      "resolved": "https://registry.npmjs.org/@emnapi/core/-/core-1.8.1.tgz",
      "integrity": "sha512-AvT9QFpxK0Zd8J0jopedNm+w/2fIzvtPKPjqyw9jwvBaReTTqPBk9Hixaz7KbjimP+QNz605/XnjFcDAL2pqBg==",
      "dev": true,
      "optional": true,
      "dependencies": {
        "@emnapi/wasi-threads": "1.1.0",
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@emnapi/runtime": {
      "version": "1.8.1",
      "resolved": "https://registry.npmjs.org/@emnapi/runtime/-/runtime-1.8.1.tgz",
      "integrity": "sha512-mehfKSMWjjNol8659Z8KxEMrdSJDDot5SXMq00dM8BN4o+CLNXQ0xH2V7EchNHV4RmbZLmmPdEaXZc5H2FXmDg==",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@emnapi/wasi-threads": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/@emnapi/wasi-threads/-/wasi-threads-1.1.0.tgz",
      "integrity": "sha512-WI0DdZ8xFSbgMjR1sFsKABJ/C5OnRrjT06JXbZKexJGrDuPTzZdDYfFlsgcCXCyf+suG5QU2e/y1Wo2V/OapLQ==",
      "dev": true,
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@eslint-community/eslint-utils": {
      "version": "4.9.1",
      "resolved": "https://registry.npmjs.org/@eslint-community/eslint-utils/-/eslint-utils-4.9.1.tgz",
      "integrity": "sha512-phrYmNiYppR7znFEdqgfWHXR6NCkZEK7hwWDHZUjit/2/U0r6XvkDl0SYnoM51Hq7FhCGdLDT6zxCCOY1hexsQ==",
      "dev": true,
      "dependencies": {
        "eslint-visitor-keys": "^3.4.3"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || >=8.0.0"
      }
    },
    "node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys": {
      "version": "3.4.3",
      "resolved": "https://registry.npmjs.org/eslint-visitor-keys/-/eslint-visitor-keys-3.4.3.tgz",
      "integrity": "sha512-wpc+LXeiyiisxPlEkUzU6svyS1frIO3Mgxj1fdy7Pm8Ygzguax2N3Fa/D/ag1WqbOprdI+uY6wMUl8/a2G+iag==",
      "dev": true,
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/@eslint-community/regexpp": {
      "version": "4.12.2",
      "resolved": "https://registry.npmjs.org/@eslint-community/regexpp/-/regexpp-4.12.2.tgz",
      "integrity": "sha512-EriSTlt5OC9/7SXkRSCAhfSxxoSUgBm33OH+IkwbdpgoqsSsUg7y3uh+IICI/Qg4BBWr3U2i39RpmycbxMq4ew==",
      "dev": true,
      "engines": {
        "node": "^12.0.0 || ^14.0.0 || >=16.0.0"
      }
    },
    "node_modules/@eslint/config-array": {
      "version": "0.21.1",
      "resolved": "https://registry.npmjs.org/@eslint/config-array/-/config-array-0.21.1.tgz",
      "integrity": "sha512-aw1gNayWpdI/jSYVgzN5pL0cfzU02GT3NBpeT/DXbx1/1x7ZKxFPd9bwrzygx/qiwIQiJ1sw/zD8qY/kRvlGHA==",
      "dev": true,
      "dependencies": {
        "@eslint/object-schema": "^2.1.7",
        "debug": "^4.3.1",
        "minimatch": "^3.1.2"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      }
    },
    "node_modules/@eslint/config-helpers": {
      "version": "0.4.2",
      "resolved": "https://registry.npmjs.org/@eslint/config-helpers/-/config-helpers-0.4.2.tgz",
      "integrity": "sha512-gBrxN88gOIf3R7ja5K9slwNayVcZgK6SOUORm2uBzTeIEfeVaIhOpCtTox3P6R7o2jLFwLFTLnC7kU/RGcYEgw==",
      "dev": true,
      "dependencies": {
        "@eslint/core": "^0.17.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      }
    },
    "node_modules/@eslint/core": {
      "version": "0.17.0",
      "resolved": "https://registry.npmjs.org/@eslint/core/-/core-0.17.0.tgz",
      "integrity": "sha512-yL/sLrpmtDaFEiUj1osRP4TI2MDz1AddJL+jZ7KSqvBuliN4xqYY54IfdN8qD8Toa6g1iloph1fxQNkjOxrrpQ==",
      "dev": true,
      "dependencies": {
        "@types/json-schema": "^7.0.15"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      }
    },
    "node_modules/@eslint/eslintrc": {
      "version": "3.3.3",
      "resolved": "https://registry.npmjs.org/@eslint/eslintrc/-/eslintrc-3.3.3.tgz",
      "integrity": "sha512-Kr+LPIUVKz2qkx1HAMH8q1q6azbqBAsXJUxBl/ODDuVPX45Z9DfwB8tPjTi6nNZ8BuM3nbJxC5zCAg5elnBUTQ==",
      "dev": true,
      "dependencies": {
        "ajv": "^6.12.4",
        "debug": "^4.3.2",
        "espree": "^10.0.1",
        "globals": "^14.0.0",
        "ignore": "^5.2.0",
        "import-fresh": "^3.2.1",
        "js-yaml": "^4.1.1",
        "minimatch": "^3.1.2",
        "strip-json-comments": "^3.1.1"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/@eslint/js": {
      "version": "9.39.2",
      "resolved": "https://registry.npmjs.org/@eslint/js/-/js-9.39.2.tgz",
      "integrity": "sha512-q1mjIoW1VX4IvSocvM/vbTiveKC4k9eLrajNEuSsmjymSDEbpGddtpfOoN7YGAqBK3NG+uqo8ia4PDTt8buCYA==",
      "dev": true,
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "url": "https://eslint.org/donate"
      }
    },
    "node_modules/@eslint/object-schema": {
      "version": "2.1.7",
      "resolved": "https://registry.npmjs.org/@eslint/object-schema/-/object-schema-2.1.7.tgz",
      "integrity": "sha512-VtAOaymWVfZcmZbp6E2mympDIHvyjXs/12LqWYjVw6qjrfF+VK+fyG33kChz3nnK+SU5/NeHOqrTEHS8sXO3OA==",
      "dev": true,
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      }
    },
    "node_modules/@eslint/plugin-kit": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/@eslint/plugin-kit/-/plugin-kit-0.4.1.tgz",
      "integrity": "sha512-43/qtrDUokr7LJqoF2c3+RInu/t4zfrpYdoSDfYyhg52rwLV6TnOvdG4fXm7IkSB3wErkcmJS9iEhjVtOSEjjA==",
      "dev": true,
      "dependencies": {
        "@eslint/core": "^0.17.0",
        "levn": "^0.4.1"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      }
    },
    "node_modules/@humanfs/core": {
      "version": "0.19.1",
      "resolved": "https://registry.npmjs.org/@humanfs/core/-/core-0.19.1.tgz",
      "integrity": "sha512-5DyQ4+1JEUzejeK1JGICcideyfUbGixgS9jNgex5nqkW+cY7WZhxBigmieN5Qnw9ZosSNVC9KQKyb+GUaGyKUA==",
      "dev": true,
      "engines": {
        "node": ">=18.18.0"
      }
    },
    "node_modules/@humanfs/node": {
      "version": "0.16.7",
      "resolved": "https://registry.npmjs.org/@humanfs/node/-/node-0.16.7.tgz",
      "integrity": "sha512-/zUx+yOsIrG4Y43Eh2peDeKCxlRt/gET6aHfaKpuq267qXdYDFViVHfMaLyygZOnl0kGWxFIgsBy8QFuTLUXEQ==",
      "dev": true,
      "dependencies": {
        "@humanfs/core": "^0.19.1",
        "@humanwhocodes/retry": "^0.4.0"
      },
      "engines": {
        "node": ">=18.18.0"
      }
    },
    "node_modules/@humanwhocodes/module-importer": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/module-importer/-/module-importer-1.0.1.tgz",
      "integrity": "sha512-bxveV4V8v5Yb4ncFTT3rPSgZBOpCkjfK0y4oVVVJwIuDVBRMDXrPyXRL988i5ap9m9bnyEEjWfm5WkBmtffLfA==",
      "dev": true,
      "engines": {
        "node": ">=12.22"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/nzakas"
      }
    },
    "node_modules/@humanwhocodes/retry": {
      "version": "0.4.3",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/retry/-/retry-0.4.3.tgz",
      "integrity": "sha512-bV0Tgo9K4hfPCek+aMAn81RppFKv2ySDQeMoSZuvTASywNTnVJCArCZE2FWqpvIatKu7VMRLWlR1EazvVhDyhQ==",
      "dev": true,
      "engines": {
        "node": ">=18.18"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/nzakas"
      }
    },
    "node_modules/@img/colour": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/@img/colour/-/colour-1.0.0.tgz",
      "integrity": "sha512-A5P/LfWGFSl6nsckYtjw9da+19jB8hkJ6ACTGcDfEJ0aE+l2n2El7dsVM7UVHZQ9s2lmYMWlrS21YLy2IR1LUw==",
      "optional": true,
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@img/sharp-darwin-arm64": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-darwin-arm64/-/sharp-darwin-arm64-0.34.5.tgz",
      "integrity": "sha512-imtQ3WMJXbMY4fxb/Ndp6HBTNVtWCUI0WdobyheGf5+ad6xX8VIDO8u2xE4qc/fr08CKG/7dDseFtn6M6g/r3w==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-libvips-darwin-arm64": "1.2.4"
      }
    },
    "node_modules/@img/sharp-darwin-x64": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-darwin-x64/-/sharp-darwin-x64-0.34.5.tgz",
      "integrity": "sha512-YNEFAF/4KQ/PeW0N+r+aVVsoIY0/qxxikF2SWdp+NRkmMB7y9LBZAVqQ4yhGCm/H3H270OSykqmQMKLBhBJDEw==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-libvips-darwin-x64": "1.2.4"
      }
    },
    "node_modules/@img/sharp-libvips-darwin-arm64": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/@img/sharp-libvips-darwin-arm64/-/sharp-libvips-darwin-arm64-1.2.4.tgz",
      "integrity": "sha512-zqjjo7RatFfFoP0MkQ51jfuFZBnVE2pRiaydKJ1G/rHZvnsrHAOcQALIi9sA5co5xenQdTugCvtb1cuf78Vf4g==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "darwin"
      ],
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-libvips-darwin-x64": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/@img/sharp-libvips-darwin-x64/-/sharp-libvips-darwin-x64-1.2.4.tgz",
      "integrity": "sha512-1IOd5xfVhlGwX+zXv2N93k0yMONvUlANylbJw1eTah8K/Jtpi15KC+WSiaX/nBmbm2HxRM1gZ0nSdjSsrZbGKg==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "darwin"
      ],
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-libvips-linux-arm": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/@img/sharp-libvips-linux-arm/-/sharp-libvips-linux-arm-1.2.4.tgz",
      "integrity": "sha512-bFI7xcKFELdiNCVov8e44Ia4u2byA+l3XtsAj+Q8tfCwO6BQ8iDojYdvoPMqsKDkuoOo+X6HZA0s0q11ANMQ8A==",
      "cpu": [
        "arm"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-libvips-linux-arm64": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/@img/sharp-libvips-linux-arm64/-/sharp-libvips-linux-arm64-1.2.4.tgz",
      "integrity": "sha512-excjX8DfsIcJ10x1Kzr4RcWe1edC9PquDRRPx3YVCvQv+U5p7Yin2s32ftzikXojb1PIFc/9Mt28/y+iRklkrw==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-libvips-linux-ppc64": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/@img/sharp-libvips-linux-ppc64/-/sharp-libvips-linux-ppc64-1.2.4.tgz",
      "integrity": "sha512-FMuvGijLDYG6lW+b/UvyilUWu5Ayu+3r2d1S8notiGCIyYU/76eig1UfMmkZ7vwgOrzKzlQbFSuQfgm7GYUPpA==",
      "cpu": [
        "ppc64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-libvips-linux-riscv64": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/@img/sharp-libvips-linux-riscv64/-/sharp-libvips-linux-riscv64-1.2.4.tgz",
      "integrity": "sha512-oVDbcR4zUC0ce82teubSm+x6ETixtKZBh/qbREIOcI3cULzDyb18Sr/Wcyx7NRQeQzOiHTNbZFF1UwPS2scyGA==",
      "cpu": [
        "riscv64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-libvips-linux-s390x": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/@img/sharp-libvips-linux-s390x/-/sharp-libvips-linux-s390x-1.2.4.tgz",
      "integrity": "sha512-qmp9VrzgPgMoGZyPvrQHqk02uyjA0/QrTO26Tqk6l4ZV0MPWIW6LTkqOIov+J1yEu7MbFQaDpwdwJKhbJvuRxQ==",
      "cpu": [
        "s390x"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-libvips-linux-x64": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/@img/sharp-libvips-linux-x64/-/sharp-libvips-linux-x64-1.2.4.tgz",
      "integrity": "sha512-tJxiiLsmHc9Ax1bz3oaOYBURTXGIRDODBqhveVHonrHJ9/+k89qbLl0bcJns+e4t4rvaNBxaEZsFtSfAdquPrw==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-libvips-linuxmusl-arm64": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/@img/sharp-libvips-linuxmusl-arm64/-/sharp-libvips-linuxmusl-arm64-1.2.4.tgz",
      "integrity": "sha512-FVQHuwx1IIuNow9QAbYUzJ+En8KcVm9Lk5+uGUQJHaZmMECZmOlix9HnH7n1TRkXMS0pGxIJokIVB9SuqZGGXw==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-libvips-linuxmusl-x64": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/@img/sharp-libvips-linuxmusl-x64/-/sharp-libvips-linuxmusl-x64-1.2.4.tgz",
      "integrity": "sha512-+LpyBk7L44ZIXwz/VYfglaX/okxezESc6UxDSoyo2Ks6Jxc4Y7sGjpgU9s4PMgqgjj1gZCylTieNamqA1MF7Dg==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-linux-arm": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-linux-arm/-/sharp-linux-arm-0.34.5.tgz",
      "integrity": "sha512-9dLqsvwtg1uuXBGZKsxem9595+ujv0sJ6Vi8wcTANSFpwV/GONat5eCkzQo/1O6zRIkh0m/8+5BjrRr7jDUSZw==",
      "cpu": [
        "arm"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-libvips-linux-arm": "1.2.4"
      }
    },
    "node_modules/@img/sharp-linux-arm64": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-linux-arm64/-/sharp-linux-arm64-0.34.5.tgz",
      "integrity": "sha512-bKQzaJRY/bkPOXyKx5EVup7qkaojECG6NLYswgktOZjaXecSAeCWiZwwiFf3/Y+O1HrauiE3FVsGxFg8c24rZg==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-libvips-linux-arm64": "1.2.4"
      }
    },
    "node_modules/@img/sharp-linux-ppc64": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-linux-ppc64/-/sharp-linux-ppc64-0.34.5.tgz",
      "integrity": "sha512-7zznwNaqW6YtsfrGGDA6BRkISKAAE1Jo0QdpNYXNMHu2+0dTrPflTLNkpc8l7MUP5M16ZJcUvysVWWrMefZquA==",
      "cpu": [
        "ppc64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-libvips-linux-ppc64": "1.2.4"
      }
    },
    "node_modules/@img/sharp-linux-riscv64": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-linux-riscv64/-/sharp-linux-riscv64-0.34.5.tgz",
      "integrity": "sha512-51gJuLPTKa7piYPaVs8GmByo7/U7/7TZOq+cnXJIHZKavIRHAP77e3N2HEl3dgiqdD/w0yUfiJnII77PuDDFdw==",
      "cpu": [
        "riscv64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-libvips-linux-riscv64": "1.2.4"
      }
    },
    "node_modules/@img/sharp-linux-s390x": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-linux-s390x/-/sharp-linux-s390x-0.34.5.tgz",
      "integrity": "sha512-nQtCk0PdKfho3eC5MrbQoigJ2gd1CgddUMkabUj+rBevs8tZ2cULOx46E7oyX+04WGfABgIwmMC0VqieTiR4jg==",
      "cpu": [
        "s390x"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-libvips-linux-s390x": "1.2.4"
      }
    },
    "node_modules/@img/sharp-linux-x64": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-linux-x64/-/sharp-linux-x64-0.34.5.tgz",
      "integrity": "sha512-MEzd8HPKxVxVenwAa+JRPwEC7QFjoPWuS5NZnBt6B3pu7EG2Ge0id1oLHZpPJdn3OQK+BQDiw9zStiHBTJQQQQ==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-libvips-linux-x64": "1.2.4"
      }
    },
    "node_modules/@img/sharp-linuxmusl-arm64": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-linuxmusl-arm64/-/sharp-linuxmusl-arm64-0.34.5.tgz",
      "integrity": "sha512-fprJR6GtRsMt6Kyfq44IsChVZeGN97gTD331weR1ex1c1rypDEABN6Tm2xa1wE6lYb5DdEnk03NZPqA7Id21yg==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-libvips-linuxmusl-arm64": "1.2.4"
      }
    },
    "node_modules/@img/sharp-linuxmusl-x64": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-linuxmusl-x64/-/sharp-linuxmusl-x64-0.34.5.tgz",
      "integrity": "sha512-Jg8wNT1MUzIvhBFxViqrEhWDGzqymo3sV7z7ZsaWbZNDLXRJZoRGrjulp60YYtV4wfY8VIKcWidjojlLcWrd8Q==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-libvips-linuxmusl-x64": "1.2.4"
      }
    },
    "node_modules/@img/sharp-wasm32": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-wasm32/-/sharp-wasm32-0.34.5.tgz",
      "integrity": "sha512-OdWTEiVkY2PHwqkbBI8frFxQQFekHaSSkUIJkwzclWZe64O1X4UlUjqqqLaPbUpMOQk6FBu/HtlGXNblIs0huw==",
      "cpu": [
        "wasm32"
      ],
      "optional": true,
      "dependencies": {
        "@emnapi/runtime": "^1.7.0"
      },
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-win32-arm64": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-win32-arm64/-/sharp-win32-arm64-0.34.5.tgz",
      "integrity": "sha512-WQ3AgWCWYSb2yt+IG8mnC6Jdk9Whs7O0gxphblsLvdhSpSTtmu69ZG1Gkb6NuvxsNACwiPV6cNSZNzt0KPsw7g==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-win32-ia32": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-win32-ia32/-/sharp-win32-ia32-0.34.5.tgz",
      "integrity": "sha512-FV9m/7NmeCmSHDD5j4+4pNI8Cp3aW+JvLoXcTUo0IqyjSfAZJ8dIUmijx1qaJsIiU+Hosw6xM5KijAWRJCSgNg==",
      "cpu": [
        "ia32"
      ],
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@img/sharp-win32-x64": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/@img/sharp-win32-x64/-/sharp-win32-x64-0.34.5.tgz",
      "integrity": "sha512-+29YMsqY2/9eFEiW93eqWnuLcWcufowXewwSNIT6UwZdUUCrM3oFjMWH/Z6/TMmb4hlFenmfAVbpWeup2jryCw==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      }
    },
    "node_modules/@jridgewell/gen-mapping": {
      "version": "0.3.13",
      "resolved": "https://registry.npmjs.org/@jridgewell/gen-mapping/-/gen-mapping-0.3.13.tgz",
      "integrity": "sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA==",
      "dev": true,
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.5.0",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/remapping": {
      "version": "2.3.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/remapping/-/remapping-2.3.5.tgz",
      "integrity": "sha512-LI9u/+laYG4Ds1TDKSJW2YPrIlcVYOwi2fUC6xB43lueCjgxV4lffOCZCtYFiH6TNOX+tQKXx97T4IKHbhyHEQ==",
      "dev": true,
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/resolve-uri": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/@jridgewell/resolve-uri/-/resolve-uri-3.1.2.tgz",
      "integrity": "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw==",
      "dev": true,
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "dev": true
    },
    "node_modules/@jridgewell/trace-mapping": {
      "version": "0.3.31",
      "resolved": "https://registry.npmjs.org/@jridgewell/trace-mapping/-/trace-mapping-0.3.31.tgz",
      "integrity": "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw==",
      "dev": true,
      "dependencies": {
        "@jridgewell/resolve-uri": "^3.1.0",
        "@jridgewell/sourcemap-codec": "^1.4.14"
      }
    },
    "node_modules/@napi-rs/wasm-runtime": {
      "version": "0.2.12",
      "resolved": "https://registry.npmjs.org/@napi-rs/wasm-runtime/-/wasm-runtime-0.2.12.tgz",
      "integrity": "sha512-ZVWUcfwY4E/yPitQJl481FjFo3K22D6qF0DuFH6Y/nbnE11GY5uguDxZMGXPQ8WQ0128MXQD7TnfHyK4oWoIJQ==",
      "dev": true,
      "optional": true,
      "dependencies": {
        "@emnapi/core": "^1.4.3",
        "@emnapi/runtime": "^1.4.3",
        "@tybys/wasm-util": "^0.10.0"
      }
    },
    "node_modules/@next/env": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/@next/env/-/env-16.1.6.tgz",
      "integrity": "sha512-N1ySLuZjnAtN3kFnwhAwPvZah8RJxKasD7x1f8shFqhncnWZn4JMfg37diLNuoHsLAlrDfM3g4mawVdtAG8XLQ=="
    },
    "node_modules/@next/eslint-plugin-next": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/@next/eslint-plugin-next/-/eslint-plugin-next-16.1.6.tgz",
      "integrity": "sha512-/Qq3PTagA6+nYVfryAtQ7/9FEr/6YVyvOtl6rZnGsbReGLf0jZU6gkpr1FuChAQpvV46a78p4cmHOVP8mbfSMQ==",
      "dev": true,
      "dependencies": {
        "fast-glob": "3.3.1"
      }
    },
    "node_modules/@next/swc-darwin-arm64": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/@next/swc-darwin-arm64/-/swc-darwin-arm64-16.1.6.tgz",
      "integrity": "sha512-wTzYulosJr/6nFnqGW7FrG3jfUUlEf8UjGA0/pyypJl42ExdVgC6xJgcXQ+V8QFn6niSG2Pb8+MIG1mZr2vczw==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-darwin-x64": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/@next/swc-darwin-x64/-/swc-darwin-x64-16.1.6.tgz",
      "integrity": "sha512-BLFPYPDO+MNJsiDWbeVzqvYd4NyuRrEYVB5k2N3JfWncuHAy2IVwMAOlVQDFjj+krkWzhY2apvmekMkfQR0CUQ==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-linux-arm64-gnu": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/@next/swc-linux-arm64-gnu/-/swc-linux-arm64-gnu-16.1.6.tgz",
      "integrity": "sha512-OJYkCd5pj/QloBvoEcJ2XiMnlJkRv9idWA/j0ugSuA34gMT6f5b7vOiCQHVRpvStoZUknhl6/UxOXL4OwtdaBw==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-linux-arm64-musl": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/@next/swc-linux-arm64-musl/-/swc-linux-arm64-musl-16.1.6.tgz",
      "integrity": "sha512-S4J2v+8tT3NIO9u2q+S0G5KdvNDjXfAv06OhfOzNDaBn5rw84DGXWndOEB7d5/x852A20sW1M56vhC/tRVbccQ==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-linux-x64-gnu": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/@next/swc-linux-x64-gnu/-/swc-linux-x64-gnu-16.1.6.tgz",
      "integrity": "sha512-2eEBDkFlMMNQnkTyPBhQOAyn2qMxyG2eE7GPH2WIDGEpEILcBPI/jdSv4t6xupSP+ot/jkfrCShLAa7+ZUPcJQ==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-linux-x64-musl": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/@next/swc-linux-x64-musl/-/swc-linux-x64-musl-16.1.6.tgz",
      "integrity": "sha512-oicJwRlyOoZXVlxmIMaTq7f8pN9QNbdes0q2FXfRsPhfCi8n8JmOZJm5oo1pwDaFbnnD421rVU409M3evFbIqg==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-win32-arm64-msvc": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/@next/swc-win32-arm64-msvc/-/swc-win32-arm64-msvc-16.1.6.tgz",
      "integrity": "sha512-gQmm8izDTPgs+DCWH22kcDmuUp7NyiJgEl18bcr8irXA5N2m2O+JQIr6f3ct42GOs9c0h8QF3L5SzIxcYAAXXw==",
      "cpu": [
        "arm64"
      ],
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@next/swc-win32-x64-msvc": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/@next/swc-win32-x64-msvc/-/swc-win32-x64-msvc-16.1.6.tgz",
      "integrity": "sha512-NRfO39AIrzBnixKbjuo2YiYhB6o9d8v/ymU9m/Xk8cyVk+k7XylniXkHwjs4s70wedVffc6bQNbufk5v0xEm0A==",
      "cpu": [
        "x64"
      ],
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/@nodelib/fs.scandir": {
      "version": "2.1.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.scandir/-/fs.scandir-2.1.5.tgz",
      "integrity": "sha512-vq24Bq3ym5HEQm2NKCr3yXDwjc7vTsEThRDnkp2DK9p1uqLR+DHurm/NOTo0KG7HYHU7eppKZj3MyqYuMBf62g==",
      "dev": true,
      "dependencies": {
        "@nodelib/fs.stat": "2.0.5",
        "run-parallel": "^1.1.9"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.stat": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.stat/-/fs.stat-2.0.5.tgz",
      "integrity": "sha512-RkhPPp2zrqDAQA/2jNhnztcPAlv64XdhIp7a7454A5ovI7Bukxgt7MX7udwAu3zg1DcpPU0rz3VV1SeaqvY4+A==",
      "dev": true,
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.walk": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.walk/-/fs.walk-1.2.8.tgz",
      "integrity": "sha512-oGB+UxlgWcgQkgwo8GcEGwemoTFt3FIO9ababBmaGwXIoBKZ+GTy0pP185beGg7Llih/NSHSV2XAs1lnznocSg==",
      "dev": true,
      "dependencies": {
        "@nodelib/fs.scandir": "2.1.5",
        "fastq": "^1.6.0"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nolyfill/is-core-module": {
      "version": "1.0.39",
      "resolved": "https://registry.npmjs.org/@nolyfill/is-core-module/-/is-core-module-1.0.39.tgz",
      "integrity": "sha512-nn5ozdjYQpUCZlWGuxcJY/KpxkWQs4DcbMCmKojjyrYDEAGy4Ce19NN4v5MduafTwJlbKc99UA8YhSVqq9yPZA==",
      "dev": true,
      "engines": {
        "node": ">=12.4.0"
      }
    },
    "node_modules/@rtsao/scc": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/@rtsao/scc/-/scc-1.1.0.tgz",
      "integrity": "sha512-zt6OdqaDoOnJ1ZYsCYGt9YmWzDXl4vQdKTyJev62gFhRGKdx7mcT54V9KIjg+d2wi9EXsPvAPKe7i7WjfVWB8g==",
      "dev": true
    },
    "node_modules/@swc/helpers": {
      "version": "0.5.15",
      "resolved": "https://registry.npmjs.org/@swc/helpers/-/helpers-0.5.15.tgz",
      "integrity": "sha512-JQ5TuMi45Owi4/BIMAJBoSQoOJu12oOk/gADqlcUL9JEdHB8vyjUSsxqeNXnmXHjYKMi2WcYtezGEEhqUI/E2g==",
      "dependencies": {
        "tslib": "^2.8.0"
      }
    },
    "node_modules/@tybys/wasm-util": {
      "version": "0.10.1",
      "resolved": "https://registry.npmjs.org/@tybys/wasm-util/-/wasm-util-0.10.1.tgz",
      "integrity": "sha512-9tTaPJLSiejZKx+Bmog4uSubteqTvFrVrURwkmHixBo0G4seD0zUxp98E1DzUBJxLQ3NPwXrGKDiVjwx/DpPsg==",
      "dev": true,
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@types/estree": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-1.0.8.tgz",
      "integrity": "sha512-dWHzHa2WqEXI/O1E9OjrocMTKJl2mSrEolh1Iomrv6U+JuNwaHXsXx9bLu5gG7BUWFIN0skIQJQ/L1rIex4X6w==",
      "dev": true
    },
    "node_modules/@types/json-schema": {
      "version": "7.0.15",
      "resolved": "https://registry.npmjs.org/@types/json-schema/-/json-schema-7.0.15.tgz",
      "integrity": "sha512-5+fP8P8MFNC+AyZCDxrB2pkZFPGzqQWUzpSeuuVLvm8VMcorNYavBqoFcxK8bQz4Qsbn4oUEEem4wDLfcysGHA==",
      "dev": true
    },
    "node_modules/@types/json5": {
      "version": "0.0.29",
      "resolved": "https://registry.npmjs.org/@types/json5/-/json5-0.0.29.tgz",
      "integrity": "sha512-dRLjCWHYg4oaA77cxO64oO+7JwCwnIzkZPdrrC71jQmQtlhM556pwKo5bUzqvZndkVbeFLIIi+9TC40JNF5hNQ==",
      "dev": true
    },
    "node_modules/@types/node": {
      "version": "20.19.30",
      "resolved": "https://registry.npmjs.org/@types/node/-/node-20.19.30.tgz",
      "integrity": "sha512-WJtwWJu7UdlvzEAUm484QNg5eAoq5QR08KDNx7g45Usrs2NtOPiX8ugDqmKdXkyL03rBqU5dYNYVQetEpBHq2g==",
      "dev": true,
      "dependencies": {
        "undici-types": "~6.21.0"
      }
    },
    "node_modules/@types/react": {
      "version": "19.2.10",
      "resolved": "https://registry.npmjs.org/@types/react/-/react-19.2.10.tgz",
      "integrity": "sha512-WPigyYuGhgZ/cTPRXB2EwUw+XvsRA3GqHlsP4qteqrnnjDrApbS7MxcGr/hke5iUoeB7E/gQtrs9I37zAJ0Vjw==",
      "dev": true,
      "dependencies": {
        "csstype": "^3.2.2"
      }
    },
    "node_modules/@types/react-dom": {
      "version": "19.2.3",
      "resolved": "https://registry.npmjs.org/@types/react-dom/-/react-dom-19.2.3.tgz",
      "integrity": "sha512-jp2L/eY6fn+KgVVQAOqYItbF0VY/YApe5Mz2F0aykSO8gx31bYCZyvSeYxCHKvzHG5eZjc+zyaS5BrBWya2+kQ==",
      "dev": true,
      "peerDependencies": {
        "@types/react": "^19.2.0"
      }
    },
    "node_modules/@typescript-eslint/eslint-plugin": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/eslint-plugin/-/eslint-plugin-8.54.0.tgz",
      "integrity": "sha512-hAAP5io/7csFStuOmR782YmTthKBJ9ND3WVL60hcOjvtGFb+HJxH4O5huAcmcZ9v9G8P+JETiZ/G1B8MALnWZQ==",
      "dev": true,
      "dependencies": {
        "@eslint-community/regexpp": "^4.12.2",
        "@typescript-eslint/scope-manager": "8.54.0",
        "@typescript-eslint/type-utils": "8.54.0",
        "@typescript-eslint/utils": "8.54.0",
        "@typescript-eslint/visitor-keys": "8.54.0",
        "ignore": "^7.0.5",
        "natural-compare": "^1.4.0",
        "ts-api-utils": "^2.4.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "@typescript-eslint/parser": "^8.54.0",
        "eslint": "^8.57.0 || ^9.0.0",
        "typescript": ">=4.8.4 <6.0.0"
      }
    },
    "node_modules/@typescript-eslint/eslint-plugin/node_modules/ignore": {
      "version": "7.0.5",
      "resolved": "https://registry.npmjs.org/ignore/-/ignore-7.0.5.tgz",
      "integrity": "sha512-Hs59xBNfUIunMFgWAbGX5cq6893IbWg4KnrjbYwX3tx0ztorVgTDA6B2sxf8ejHJ4wz8BqGUMYlnzNBer5NvGg==",
      "dev": true,
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/@typescript-eslint/parser": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/parser/-/parser-8.54.0.tgz",
      "integrity": "sha512-BtE0k6cjwjLZoZixN0t5AKP0kSzlGu7FctRXYuPAm//aaiZhmfq1JwdYpYr1brzEspYyFeF+8XF5j2VK6oalrA==",
      "dev": true,
      "dependencies": {
        "@typescript-eslint/scope-manager": "8.54.0",
        "@typescript-eslint/types": "8.54.0",
        "@typescript-eslint/typescript-estree": "8.54.0",
        "@typescript-eslint/visitor-keys": "8.54.0",
        "debug": "^4.4.3"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^8.57.0 || ^9.0.0",
        "typescript": ">=4.8.4 <6.0.0"
      }
    },
    "node_modules/@typescript-eslint/project-service": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/project-service/-/project-service-8.54.0.tgz",
      "integrity": "sha512-YPf+rvJ1s7MyiWM4uTRhE4DvBXrEV+d8oC3P9Y2eT7S+HBS0clybdMIPnhiATi9vZOYDc7OQ1L/i6ga6NFYK/g==",
      "dev": true,
      "dependencies": {
        "@typescript-eslint/tsconfig-utils": "^8.54.0",
        "@typescript-eslint/types": "^8.54.0",
        "debug": "^4.4.3"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "typescript": ">=4.8.4 <6.0.0"
      }
    },
    "node_modules/@typescript-eslint/scope-manager": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/scope-manager/-/scope-manager-8.54.0.tgz",
      "integrity": "sha512-27rYVQku26j/PbHYcVfRPonmOlVI6gihHtXFbTdB5sb6qA0wdAQAbyXFVarQ5t4HRojIz64IV90YtsjQSSGlQg==",
      "dev": true,
      "dependencies": {
        "@typescript-eslint/types": "8.54.0",
        "@typescript-eslint/visitor-keys": "8.54.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@typescript-eslint/tsconfig-utils": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/tsconfig-utils/-/tsconfig-utils-8.54.0.tgz",
      "integrity": "sha512-dRgOyT2hPk/JwxNMZDsIXDgyl9axdJI3ogZ2XWhBPsnZUv+hPesa5iuhdYt2gzwA9t8RE5ytOJ6xB0moV0Ujvw==",
      "dev": true,
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "typescript": ">=4.8.4 <6.0.0"
      }
    },
    "node_modules/@typescript-eslint/type-utils": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/type-utils/-/type-utils-8.54.0.tgz",
      "integrity": "sha512-hiLguxJWHjjwL6xMBwD903ciAwd7DmK30Y9Axs/etOkftC3ZNN9K44IuRD/EB08amu+Zw6W37x9RecLkOo3pMA==",
      "dev": true,
      "dependencies": {
        "@typescript-eslint/types": "8.54.0",
        "@typescript-eslint/typescript-estree": "8.54.0",
        "@typescript-eslint/utils": "8.54.0",
        "debug": "^4.4.3",
        "ts-api-utils": "^2.4.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^8.57.0 || ^9.0.0",
        "typescript": ">=4.8.4 <6.0.0"
      }
    },
    "node_modules/@typescript-eslint/types": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/types/-/types-8.54.0.tgz",
      "integrity": "sha512-PDUI9R1BVjqu7AUDsRBbKMtwmjWcn4J3le+5LpcFgWULN3LvHC5rkc9gCVxbrsrGmO1jfPybN5s6h4Jy+OnkAA==",
      "dev": true,
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@typescript-eslint/typescript-estree": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/typescript-estree/-/typescript-estree-8.54.0.tgz",
      "integrity": "sha512-BUwcskRaPvTk6fzVWgDPdUndLjB87KYDrN5EYGetnktoeAvPtO4ONHlAZDnj5VFnUANg0Sjm7j4usBlnoVMHwA==",
      "dev": true,
      "dependencies": {
        "@typescript-eslint/project-service": "8.54.0",
        "@typescript-eslint/tsconfig-utils": "8.54.0",
        "@typescript-eslint/types": "8.54.0",
        "@typescript-eslint/visitor-keys": "8.54.0",
        "debug": "^4.4.3",
        "minimatch": "^9.0.5",
        "semver": "^7.7.3",
        "tinyglobby": "^0.2.15",
        "ts-api-utils": "^2.4.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "typescript": ">=4.8.4 <6.0.0"
      }
    },
    "node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-2.0.2.tgz",
      "integrity": "sha512-Jt0vHyM+jmUBqojB7E1NIYadt0vI0Qxjxd2TErW94wDz+E2LAm5vKMXXwg6ZZBTHPuUlDgQHKXvjGBdfcF1ZDQ==",
      "dev": true,
      "dependencies": {
        "balanced-match": "^1.0.0"
      }
    },
    "node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch": {
      "version": "9.0.5",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-9.0.5.tgz",
      "integrity": "sha512-G6T0ZX48xgozx7587koeX9Ys2NYy6Gmv//P89sEte9V9whIapMNF4idKxnW2QtCcLiTWlb/wfCabAtAFWhhBow==",
      "dev": true,
      "dependencies": {
        "brace-expansion": "^2.0.1"
      },
      "engines": {
        "node": ">=16 || 14 >=14.17"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/@typescript-eslint/typescript-estree/node_modules/semver": {
      "version": "7.7.3",
      "resolved": "https://registry.npmjs.org/semver/-/semver-7.7.3.tgz",
      "integrity": "sha512-SdsKMrI9TdgjdweUSR9MweHA4EJ8YxHn8DFaDisvhVlUOe4BF1tLD7GAj0lIqWVl+dPb/rExr0Btby5loQm20Q==",
      "dev": true,
      "bin": {
        "semver": "bin/semver.js"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/@typescript-eslint/utils": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/utils/-/utils-8.54.0.tgz",
      "integrity": "sha512-9Cnda8GS57AQakvRyG0PTejJNlA2xhvyNtEVIMlDWOOeEyBkYWhGPnfrIAnqxLMTSTo6q8g12XVjjev5l1NvMA==",
      "dev": true,
      "dependencies": {
        "@eslint-community/eslint-utils": "^4.9.1",
        "@typescript-eslint/scope-manager": "8.54.0",
        "@typescript-eslint/types": "8.54.0",
        "@typescript-eslint/typescript-estree": "8.54.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^8.57.0 || ^9.0.0",
        "typescript": ">=4.8.4 <6.0.0"
      }
    },
    "node_modules/@typescript-eslint/visitor-keys": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/visitor-keys/-/visitor-keys-8.54.0.tgz",
      "integrity": "sha512-VFlhGSl4opC0bprJiItPQ1RfUhGDIBokcPwaFH4yiBCaNPeld/9VeXbiPO1cLyorQi1G1vL+ecBk1x8o1axORA==",
      "dev": true,
      "dependencies": {
        "@typescript-eslint/types": "8.54.0",
        "eslint-visitor-keys": "^4.2.1"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@unrs/resolver-binding-android-arm-eabi": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-android-arm-eabi/-/resolver-binding-android-arm-eabi-1.11.1.tgz",
      "integrity": "sha512-ppLRUgHVaGRWUx0R0Ut06Mjo9gBaBkg3v/8AxusGLhsIotbBLuRk51rAzqLC8gq6NyyAojEXglNjzf6R948DNw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@unrs/resolver-binding-android-arm64": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-android-arm64/-/resolver-binding-android-arm64-1.11.1.tgz",
      "integrity": "sha512-lCxkVtb4wp1v+EoN+HjIG9cIIzPkX5OtM03pQYkG+U5O/wL53LC4QbIeazgiKqluGeVEeBlZahHalCaBvU1a2g==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@unrs/resolver-binding-darwin-arm64": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-darwin-arm64/-/resolver-binding-darwin-arm64-1.11.1.tgz",
      "integrity": "sha512-gPVA1UjRu1Y/IsB/dQEsp2V1pm44Of6+LWvbLc9SDk1c2KhhDRDBUkQCYVWe6f26uJb3fOK8saWMgtX8IrMk3g==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@unrs/resolver-binding-darwin-x64": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-darwin-x64/-/resolver-binding-darwin-x64-1.11.1.tgz",
      "integrity": "sha512-cFzP7rWKd3lZaCsDze07QX1SC24lO8mPty9vdP+YVa3MGdVgPmFc59317b2ioXtgCMKGiCLxJ4HQs62oz6GfRQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@unrs/resolver-binding-freebsd-x64": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-freebsd-x64/-/resolver-binding-freebsd-x64-1.11.1.tgz",
      "integrity": "sha512-fqtGgak3zX4DCB6PFpsH5+Kmt/8CIi4Bry4rb1ho6Av2QHTREM+47y282Uqiu3ZRF5IQioJQ5qWRV6jduA+iGw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "freebsd"
      ]
    },
    "node_modules/@unrs/resolver-binding-linux-arm-gnueabihf": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-linux-arm-gnueabihf/-/resolver-binding-linux-arm-gnueabihf-1.11.1.tgz",
      "integrity": "sha512-u92mvlcYtp9MRKmP+ZvMmtPN34+/3lMHlyMj7wXJDeXxuM0Vgzz0+PPJNsro1m3IZPYChIkn944wW8TYgGKFHw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@unrs/resolver-binding-linux-arm-musleabihf": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-linux-arm-musleabihf/-/resolver-binding-linux-arm-musleabihf-1.11.1.tgz",
      "integrity": "sha512-cINaoY2z7LVCrfHkIcmvj7osTOtm6VVT16b5oQdS4beibX2SYBwgYLmqhBjA1t51CarSaBuX5YNsWLjsqfW5Cw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@unrs/resolver-binding-linux-arm64-gnu": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-linux-arm64-gnu/-/resolver-binding-linux-arm64-gnu-1.11.1.tgz",
      "integrity": "sha512-34gw7PjDGB9JgePJEmhEqBhWvCiiWCuXsL9hYphDF7crW7UgI05gyBAi6MF58uGcMOiOqSJ2ybEeCvHcq0BCmQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@unrs/resolver-binding-linux-arm64-musl": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-linux-arm64-musl/-/resolver-binding-linux-arm64-musl-1.11.1.tgz",
      "integrity": "sha512-RyMIx6Uf53hhOtJDIamSbTskA99sPHS96wxVE/bJtePJJtpdKGXO1wY90oRdXuYOGOTuqjT8ACccMc4K6QmT3w==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@unrs/resolver-binding-linux-ppc64-gnu": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-linux-ppc64-gnu/-/resolver-binding-linux-ppc64-gnu-1.11.1.tgz",
      "integrity": "sha512-D8Vae74A4/a+mZH0FbOkFJL9DSK2R6TFPC9M+jCWYia/q2einCubX10pecpDiTmkJVUH+y8K3BZClycD8nCShA==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@unrs/resolver-binding-linux-riscv64-gnu": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-linux-riscv64-gnu/-/resolver-binding-linux-riscv64-gnu-1.11.1.tgz",
      "integrity": "sha512-frxL4OrzOWVVsOc96+V3aqTIQl1O2TjgExV4EKgRY09AJ9leZpEg8Ak9phadbuX0BA4k8U5qtvMSQQGGmaJqcQ==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@unrs/resolver-binding-linux-riscv64-musl": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-linux-riscv64-musl/-/resolver-binding-linux-riscv64-musl-1.11.1.tgz",
      "integrity": "sha512-mJ5vuDaIZ+l/acv01sHoXfpnyrNKOk/3aDoEdLO/Xtn9HuZlDD6jKxHlkN8ZhWyLJsRBxfv9GYM2utQ1SChKew==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@unrs/resolver-binding-linux-s390x-gnu": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-linux-s390x-gnu/-/resolver-binding-linux-s390x-gnu-1.11.1.tgz",
      "integrity": "sha512-kELo8ebBVtb9sA7rMe1Cph4QHreByhaZ2QEADd9NzIQsYNQpt9UkM9iqr2lhGr5afh885d/cB5QeTXSbZHTYPg==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@unrs/resolver-binding-linux-x64-gnu": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-linux-x64-gnu/-/resolver-binding-linux-x64-gnu-1.11.1.tgz",
      "integrity": "sha512-C3ZAHugKgovV5YvAMsxhq0gtXuwESUKc5MhEtjBpLoHPLYM+iuwSj3lflFwK3DPm68660rZ7G8BMcwSro7hD5w==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@unrs/resolver-binding-linux-x64-musl": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-linux-x64-musl/-/resolver-binding-linux-x64-musl-1.11.1.tgz",
      "integrity": "sha512-rV0YSoyhK2nZ4vEswT/QwqzqQXw5I6CjoaYMOX0TqBlWhojUf8P94mvI7nuJTeaCkkds3QE4+zS8Ko+GdXuZtA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@unrs/resolver-binding-wasm32-wasi": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-wasm32-wasi/-/resolver-binding-wasm32-wasi-1.11.1.tgz",
      "integrity": "sha512-5u4RkfxJm+Ng7IWgkzi3qrFOvLvQYnPBmjmZQ8+szTK/b31fQCnleNl1GgEt7nIsZRIf5PLhPwT0WM+q45x/UQ==",
      "cpu": [
        "wasm32"
      ],
      "dev": true,
      "optional": true,
      "dependencies": {
        "@napi-rs/wasm-runtime": "^0.2.11"
      },
      "engines": {
        "node": ">=14.0.0"
      }
    },
    "node_modules/@unrs/resolver-binding-win32-arm64-msvc": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-win32-arm64-msvc/-/resolver-binding-win32-arm64-msvc-1.11.1.tgz",
      "integrity": "sha512-nRcz5Il4ln0kMhfL8S3hLkxI85BXs3o8EYoattsJNdsX4YUU89iOkVn7g0VHSRxFuVMdM4Q1jEpIId1Ihim/Uw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@unrs/resolver-binding-win32-ia32-msvc": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-win32-ia32-msvc/-/resolver-binding-win32-ia32-msvc-1.11.1.tgz",
      "integrity": "sha512-DCEI6t5i1NmAZp6pFonpD5m7i6aFrpofcp4LA2i8IIq60Jyo28hamKBxNrZcyOwVOZkgsRp9O2sXWBWP8MnvIQ==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@unrs/resolver-binding-win32-x64-msvc": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@unrs/resolver-binding-win32-x64-msvc/-/resolver-binding-win32-x64-msvc-1.11.1.tgz",
      "integrity": "sha512-lrW200hZdbfRtztbygyaq/6jP6AKE8qQN2KvPcJ+x7wiD038YtnYtZ82IMNJ69GJibV7bwL3y9FgK+5w/pYt6g==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/acorn": {
      "version": "8.15.0",
      "resolved": "https://registry.npmjs.org/acorn/-/acorn-8.15.0.tgz",
      "integrity": "sha512-NZyJarBfL7nWwIq+FDL6Zp/yHEhePMNnnJ0y3qfieCrmNvYct8uvtiV41UvlSe6apAfk0fY1FbWx+NwfmpvtTg==",
      "dev": true,
      "bin": {
        "acorn": "bin/acorn"
      },
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/acorn-jsx": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/acorn-jsx/-/acorn-jsx-5.3.2.tgz",
      "integrity": "sha512-rq9s+JNhf0IChjtDXxllJ7g41oZk5SlXtp0LHwyA5cejwn7vKmKp4pPri6YEePv2PU65sAsegbXtIinmDFDXgQ==",
      "dev": true,
      "peerDependencies": {
        "acorn": "^6.0.0 || ^7.0.0 || ^8.0.0"
      }
    },
    "node_modules/ajv": {
      "version": "6.12.6",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-6.12.6.tgz",
      "integrity": "sha512-j3fVLgvTo527anyYyJOGTYJbG+vnnQYvE0m5mmkc1TK+nxAppkCLMIL0aZ4dblVCNoGShhm+kzE4ZUykBoMg4g==",
      "dev": true,
      "dependencies": {
        "fast-deep-equal": "^3.1.1",
        "fast-json-stable-stringify": "^2.0.0",
        "json-schema-traverse": "^0.4.1",
        "uri-js": "^4.2.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/ansi-styles": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-4.3.0.tgz",
      "integrity": "sha512-zbB9rCJAT1rbjiVDb2hqKFHNYLxgtk8NURxZ3IZwD3F6NtxbXZQCnnSi1Lkx+IDohdPlFp222wVALIheZJQSEg==",
      "dev": true,
      "dependencies": {
        "color-convert": "^2.0.1"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/any-promise": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/any-promise/-/any-promise-1.3.0.tgz",
      "integrity": "sha512-7UvmKalWRt1wgjL1RrGxoSJW/0QZFIegpeGvZG9kjp8vrRu55XTHbwnqq2GpXm9uLbcuhxm3IqX9OB4MZR1b2A==",
      "dev": true
    },
    "node_modules/anymatch": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/anymatch/-/anymatch-3.1.3.tgz",
      "integrity": "sha512-KMReFUr0B4t+D+OBkjR3KYqvocp2XaSzO55UcB6mgQMd3KbcE+mWTyvVV7D/zsdEbNnV6acZUutkiHQXvTr1Rw==",
      "dev": true,
      "dependencies": {
        "normalize-path": "^3.0.0",
        "picomatch": "^2.0.4"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/arg": {
      "version": "5.0.2",
      "resolved": "https://registry.npmjs.org/arg/-/arg-5.0.2.tgz",
      "integrity": "sha512-PYjyFOLKQ9y57JvQ6QLo8dAgNqswh8M1RMJYdQduT6xbWSgK36P/Z/v+p888pM69jMMfS8Xd8F6I1kQ/I9HUGg==",
      "dev": true
    },
    "node_modules/argparse": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/argparse/-/argparse-2.0.1.tgz",
      "integrity": "sha512-8+9WqebbFzpX9OR+Wa6O29asIogeRMzcGtAINdpMHHyAg10f05aSFVBbcEqGf/PXw1EjAZ+q2/bEBg3DvurK3Q==",
      "dev": true
    },
    "node_modules/aria-query": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/aria-query/-/aria-query-5.3.2.tgz",
      "integrity": "sha512-COROpnaoap1E2F000S62r6A60uHZnmlvomhfyT2DlTcrY1OrBKn2UhH7qn5wTC9zMvD0AY7csdPSNwKP+7WiQw==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/array-buffer-byte-length": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/array-buffer-byte-length/-/array-buffer-byte-length-1.0.2.tgz",
      "integrity": "sha512-LHE+8BuR7RYGDKvnrmcuSq3tDcKv9OFEXQt/HpbZhY7V6h0zlUXutnAD82GiFx9rdieCMjkvtcsPqBwgUl1Iiw==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3",
        "is-array-buffer": "^3.0.5"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array-includes": {
      "version": "3.1.9",
      "resolved": "https://registry.npmjs.org/array-includes/-/array-includes-3.1.9.tgz",
      "integrity": "sha512-FmeCCAenzH0KH381SPT5FZmiA/TmpndpcaShhfgEN9eCVjnFBqq3l1xrI42y8+PPLI6hypzou4GXw00WHmPBLQ==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.24.0",
        "es-object-atoms": "^1.1.1",
        "get-intrinsic": "^1.3.0",
        "is-string": "^1.1.1",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.findlast": {
      "version": "1.2.5",
      "resolved": "https://registry.npmjs.org/array.prototype.findlast/-/array.prototype.findlast-1.2.5.tgz",
      "integrity": "sha512-CVvd6FHg1Z3POpBLxO6E6zr+rSKEQ9L6rZHAaY7lLfhKsWYUBBOuMs0e9o24oopj6H+geRCX0YJ+TJLBK2eHyQ==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.2",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.findlastindex": {
      "version": "1.2.6",
      "resolved": "https://registry.npmjs.org/array.prototype.findlastindex/-/array.prototype.findlastindex-1.2.6.tgz",
      "integrity": "sha512-F/TKATkzseUExPlfvmwQKGITM3DGTK+vkAsCZoDc5daVygbJBnjEUCbgkAvVFsgfXfX4YIqZ/27G3k3tdXrTxQ==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.9",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "es-shim-unscopables": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.flat": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/array.prototype.flat/-/array.prototype.flat-1.3.3.tgz",
      "integrity": "sha512-rwG/ja1neyLqCuGZ5YYrznA62D4mZXg0i1cIskIUKSiqF3Cje9/wXAls9B9s1Wa2fomMsIv8czB8jZcPmxCXFg==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.flatmap": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/array.prototype.flatmap/-/array.prototype.flatmap-1.3.3.tgz",
      "integrity": "sha512-Y7Wt51eKJSyi80hFrJCePGGNo5ktJCslFuboqJsbf57CCPcm5zztluPlc4/aD8sWsKvlwatezpV4U1efk8kpjg==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.tosorted": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/array.prototype.tosorted/-/array.prototype.tosorted-1.1.4.tgz",
      "integrity": "sha512-p6Fx8B7b7ZhL/gmUsAy0D15WhvDccw3mnGNbZpi3pmeJdxtWsj2jEaI4Y6oo3XiHfzuSgPwKc04MYt6KgvC/wA==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.3",
        "es-errors": "^1.3.0",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/arraybuffer.prototype.slice": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/arraybuffer.prototype.slice/-/arraybuffer.prototype.slice-1.0.4.tgz",
      "integrity": "sha512-BNoCY6SXXPQ7gF2opIP4GBE+Xw7U+pHMYKuzjgCN3GwiaIR09UUeKfheyIry77QtrCBlC0KK0q5/TER/tYh3PQ==",
      "dev": true,
      "dependencies": {
        "array-buffer-byte-length": "^1.0.1",
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6",
        "is-array-buffer": "^3.0.4"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/ast-types-flow": {
      "version": "0.0.8",
      "resolved": "https://registry.npmjs.org/ast-types-flow/-/ast-types-flow-0.0.8.tgz",
      "integrity": "sha512-OH/2E5Fg20h2aPrbe+QL8JZQFko0YZaF+j4mnQ7BGhfavO7OpSLa8a0y9sBwomHdSbkhTS8TQNayBfnW5DwbvQ==",
      "dev": true
    },
    "node_modules/async-function": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/async-function/-/async-function-1.0.0.tgz",
      "integrity": "sha512-hsU18Ae8CDTR6Kgu9DYf0EbCr/a5iGL0rytQDobUcdpYOKokk8LEjVphnXkDkgpi0wYVsqrXuP0bZxJaTqdgoA==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/autoprefixer": {
      "version": "10.4.23",
      "resolved": "https://registry.npmjs.org/autoprefixer/-/autoprefixer-10.4.23.tgz",
      "integrity": "sha512-YYTXSFulfwytnjAPlw8QHncHJmlvFKtczb8InXaAx9Q0LbfDnfEYDE55omerIJKihhmU61Ft+cAOSzQVaBUmeA==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/autoprefixer"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "dependencies": {
        "browserslist": "^4.28.1",
        "caniuse-lite": "^1.0.30001760",
        "fraction.js": "^5.3.4",
        "picocolors": "^1.1.1",
        "postcss-value-parser": "^4.2.0"
      },
      "bin": {
        "autoprefixer": "bin/autoprefixer"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/available-typed-arrays": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/available-typed-arrays/-/available-typed-arrays-1.0.7.tgz",
      "integrity": "sha512-wvUjBtSGN7+7SjNpq/9M2Tg350UZD3q62IFZLbRAR1bSMlCo1ZaeW+BJ+D090e4hIIZLBcTDWe4Mh4jvUDajzQ==",
      "dev": true,
      "dependencies": {
        "possible-typed-array-names": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/axe-core": {
      "version": "4.11.1",
      "resolved": "https://registry.npmjs.org/axe-core/-/axe-core-4.11.1.tgz",
      "integrity": "sha512-BASOg+YwO2C+346x3LZOeoovTIoTrRqEsqMa6fmfAV0P+U9mFr9NsyOEpiYvFjbc64NMrSswhV50WdXzdb/Z5A==",
      "dev": true,
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/axobject-query": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/axobject-query/-/axobject-query-4.1.0.tgz",
      "integrity": "sha512-qIj0G9wZbMGNLjLmg1PT6v2mE9AH2zlnADJD/2tC6E00hgmhUOfEB6greHPAfLRSufHqROIUTkw6E+M3lH0PTQ==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/balanced-match": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/balanced-match/-/balanced-match-1.0.2.tgz",
      "integrity": "sha512-3oSeUO0TMV67hN1AmbXsK4yaqU7tjiHlbxRDZOpH0KW9+CeX4bRAaX0Anxt0tx2MrpRpWwQaPwIlISEJhYU5Pw==",
      "dev": true
    },
    "node_modules/baseline-browser-mapping": {
      "version": "2.9.19",
      "resolved": "https://registry.npmjs.org/baseline-browser-mapping/-/baseline-browser-mapping-2.9.19.tgz",
      "integrity": "sha512-ipDqC8FrAl/76p2SSWKSI+H9tFwm7vYqXQrItCuiVPt26Km0jS+NzSsBWAaBusvSbQcfJG+JitdMm+wZAgTYqg==",
      "bin": {
        "baseline-browser-mapping": "dist/cli.js"
      }
    },
    "node_modules/binary-extensions": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/binary-extensions/-/binary-extensions-2.3.0.tgz",
      "integrity": "sha512-Ceh+7ox5qe7LJuLHoY0feh3pHuUDHAcRUeyL2VYghZwfpkNIy/+8Ocg0a3UuSoYzavmylwuLWQOf3hl0jjMMIw==",
      "dev": true,
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/brace-expansion": {
      "version": "1.1.12",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.12.tgz",
      "integrity": "sha512-9T9UjW3r0UW5c1Q7GTwllptXwhvYmEzFhzMfZ9H7FQWt+uZePjZPjBP/W1ZEyZ1twGWom5/56TF4lPcqjnDHcg==",
      "dev": true,
      "dependencies": {
        "balanced-match": "^1.0.0",
        "concat-map": "0.0.1"
      }
    },
    "node_modules/braces": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/braces/-/braces-3.0.3.tgz",
      "integrity": "sha512-yQbXgO/OSZVD2IsiLlro+7Hf6Q18EJrKSEsdoMzKePKXct3gvD8oLcOQdIzGupr5Fj+EDe8gO/lxc1BzfMpxvA==",
      "dev": true,
      "dependencies": {
        "fill-range": "^7.1.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/browserslist": {
      "version": "4.28.1",
      "resolved": "https://registry.npmjs.org/browserslist/-/browserslist-4.28.1.tgz",
      "integrity": "sha512-ZC5Bd0LgJXgwGqUknZY/vkUQ04r8NXnJZ3yYi4vDmSiZmC/pdSN0NbNRPxZpbtO4uAfDUAFffO8IZoM3Gj8IkA==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "dependencies": {
        "baseline-browser-mapping": "^2.9.0",
        "caniuse-lite": "^1.0.30001759",
        "electron-to-chromium": "^1.5.263",
        "node-releases": "^2.0.27",
        "update-browserslist-db": "^1.2.0"
      },
      "bin": {
        "browserslist": "cli.js"
      },
      "engines": {
        "node": "^6 || ^7 || ^8 || ^9 || ^10 || ^11 || ^12 || >=13.7"
      }
    },
    "node_modules/call-bind": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/call-bind/-/call-bind-1.0.8.tgz",
      "integrity": "sha512-oKlSFMcMwpUg2ednkhQ454wfWiU/ul3CkJe/PEHcTKuiX6RpbehUiFMXu13HalGZxfUwCQzZG747YXBn1im9ww==",
      "dev": true,
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.0",
        "es-define-property": "^1.0.0",
        "get-intrinsic": "^1.2.4",
        "set-function-length": "^1.2.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/call-bind-apply-helpers": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/call-bind-apply-helpers/-/call-bind-apply-helpers-1.0.2.tgz",
      "integrity": "sha512-Sp1ablJ0ivDkSzjcaJdxEunN5/XvksFJ2sMBFfq6x0ryhQV/2b/KwFe21cMpmHtPOSij8K99/wSfoEuTObmuMQ==",
      "dev": true,
      "dependencies": {
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/call-bound": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/call-bound/-/call-bound-1.0.4.tgz",
      "integrity": "sha512-+ys997U96po4Kx/ABpBCqhA9EuxJaQWDQg7295H4hBphv3IZg0boBKuwYpt4YXp6MZ5AmZQnU/tyMTlRpaSejg==",
      "dev": true,
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "get-intrinsic": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/callsites": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/callsites/-/callsites-3.1.0.tgz",
      "integrity": "sha512-P8BjAsXvZS+VIDUI11hHCQEv74YT67YUi5JJFNWIqL235sBmjX4+qx9Muvls5ivyNENctx46xQLQ3aTuE7ssaQ==",
      "dev": true,
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/camelcase-css": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/camelcase-css/-/camelcase-css-2.0.1.tgz",
      "integrity": "sha512-QOSvevhslijgYwRx6Rv7zKdMF8lbRmx+uQGx2+vDc+KI/eBnsy9kit5aj23AgGu3pa4t9AgwbnXWqS+iOY+2aA==",
      "dev": true,
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/caniuse-lite": {
      "version": "1.0.30001766",
      "resolved": "https://registry.npmjs.org/caniuse-lite/-/caniuse-lite-1.0.30001766.tgz",
      "integrity": "sha512-4C0lfJ0/YPjJQHagaE9x2Elb69CIqEPZeG0anQt9SIvIoOH4a4uaRl73IavyO+0qZh6MDLH//DrXThEYKHkmYA==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/caniuse-lite"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ]
    },
    "node_modules/chalk": {
      "version": "4.1.2",
      "resolved": "https://registry.npmjs.org/chalk/-/chalk-4.1.2.tgz",
      "integrity": "sha512-oKnbhFyRIXpUuez8iBMmyEa4nbj4IOQyuhc/wy9kY7/WVPcwIO9VA668Pu8RkO7+0G76SLROeyw9CpQ061i4mA==",
      "dev": true,
      "dependencies": {
        "ansi-styles": "^4.1.0",
        "supports-color": "^7.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/chalk?sponsor=1"
      }
    },
    "node_modules/chokidar": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/chokidar/-/chokidar-3.6.0.tgz",
      "integrity": "sha512-7VT13fmjotKpGipCW9JEQAusEPE+Ei8nl6/g4FBAmIm0GOOLMua9NDDo/DWp0ZAxCr3cPq5ZpBqmPAQgDda2Pw==",
      "dev": true,
      "dependencies": {
        "anymatch": "~3.1.2",
        "braces": "~3.0.2",
        "glob-parent": "~5.1.2",
        "is-binary-path": "~2.1.0",
        "is-glob": "~4.0.1",
        "normalize-path": "~3.0.0",
        "readdirp": "~3.6.0"
      },
      "engines": {
        "node": ">= 8.10.0"
      },
      "funding": {
        "url": "https://paulmillr.com/funding/"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/chokidar/node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "dev": true,
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/client-only": {
      "version": "0.0.1",
      "resolved": "https://registry.npmjs.org/client-only/-/client-only-0.0.1.tgz",
      "integrity": "sha512-IV3Ou0jSMzZrd3pZ48nLkT9DA7Ag1pnPzaiQhpW7c3RbcqqzvzzVu+L8gfqMp/8IM2MQtSiqaCxrrcfu8I8rMA=="
    },
    "node_modules/color-convert": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/color-convert/-/color-convert-2.0.1.tgz",
      "integrity": "sha512-RRECPsj7iu/xb5oKYcsFHSppFNnsj/52OVTRKb4zP5onXwVF3zVmmToNcOfGC+CRDpfK/U584fMg38ZHCaElKQ==",
      "dev": true,
      "dependencies": {
        "color-name": "~1.1.4"
      },
      "engines": {
        "node": ">=7.0.0"
      }
    },
    "node_modules/color-name": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/color-name/-/color-name-1.1.4.tgz",
      "integrity": "sha512-dOy+3AuW3a2wNbZHIuMZpTcgjGuLU/uBL/ubcZF9OXbDo8ff4O8yVp5Bf0efS8uEoYo5q4Fx7dY9OgQGXgAsQA==",
      "dev": true
    },
    "node_modules/commander": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/commander/-/commander-4.1.1.tgz",
      "integrity": "sha512-NOKm8xhkzAjzFx8B2v5OAHT+u5pRQc2UCa2Vq9jYL/31o2wi9mxBA7LIFs3sV5VSC49z6pEhfbMULvShKj26WA==",
      "dev": true,
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/concat-map": {
      "version": "0.0.1",
      "resolved": "https://registry.npmjs.org/concat-map/-/concat-map-0.0.1.tgz",
      "integrity": "sha512-/Srv4dswyQNBfohGpz9o6Yb3Gz3SrUDqBH5rTuhGR7ahtlbYKnVxw2bCFMRljaA7EXHaXZ8wsHdodFvbkhKmqg==",
      "dev": true
    },
    "node_modules/convert-source-map": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-2.0.0.tgz",
      "integrity": "sha512-Kvp459HrV2FEJ1CAsi1Ku+MY3kasH19TFykTz2xWmMeq6bk2NU3XXvfJ+Q61m0xktWwt+1HSYf3JZsTms3aRJg==",
      "dev": true
    },
    "node_modules/cross-spawn": {
      "version": "7.0.6",
      "resolved": "https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz",
      "integrity": "sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==",
      "dev": true,
      "dependencies": {
        "path-key": "^3.1.0",
        "shebang-command": "^2.0.0",
        "which": "^2.0.1"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/cssesc": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/cssesc/-/cssesc-3.0.0.tgz",
      "integrity": "sha512-/Tb/JcjK111nNScGob5MNtsntNM1aCNUDipB/TkwZFhyDrrE47SOx/18wF2bbjgc3ZzCSKW1T5nt5EbFoAz/Vg==",
      "dev": true,
      "bin": {
        "cssesc": "bin/cssesc"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/csstype": {
      "version": "3.2.3",
      "resolved": "https://registry.npmjs.org/csstype/-/csstype-3.2.3.tgz",
      "integrity": "sha512-z1HGKcYy2xA8AGQfwrn0PAy+PB7X/GSj3UVJW9qKyn43xWa+gl5nXmU4qqLMRzWVLFC8KusUX8T/0kCiOYpAIQ==",
      "dev": true
    },
    "node_modules/damerau-levenshtein": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/damerau-levenshtein/-/damerau-levenshtein-1.0.8.tgz",
      "integrity": "sha512-sdQSFB7+llfUcQHUQO3+B8ERRj0Oa4w9POWMI/puGtuf7gFywGmkaLCElnudfTiKZV+NvHqL0ifzdrI8Ro7ESA==",
      "dev": true
    },
    "node_modules/data-view-buffer": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/data-view-buffer/-/data-view-buffer-1.0.2.tgz",
      "integrity": "sha512-EmKO5V3OLXh1rtK2wgXRansaK1/mtVdTUEiEI0W8RkvgT05kfxaH29PliLnpLP73yYO6142Q72QNa8Wx/A5CqQ==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/data-view-byte-length": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/data-view-byte-length/-/data-view-byte-length-1.0.2.tgz",
      "integrity": "sha512-tuhGbE6CfTM9+5ANGf+oQb72Ky/0+s3xKUpHvShfiz2RxMFgFPjsXuRLBVMtvMs15awe45SRb83D6wH4ew6wlQ==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/inspect-js"
      }
    },
    "node_modules/data-view-byte-offset": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/data-view-byte-offset/-/data-view-byte-offset-1.0.1.tgz",
      "integrity": "sha512-BS8PfmtDGnrgYdOonGZQdLZslWIeCGFP9tpan0hi1Co2Zr2NKADsvGYA8XxuG/4UWgJ6Cjtv+YJnB6MM69QGlQ==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/debug": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/debug/-/debug-4.4.3.tgz",
      "integrity": "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA==",
      "dev": true,
      "dependencies": {
        "ms": "^2.1.3"
      },
      "engines": {
        "node": ">=6.0"
      },
      "peerDependenciesMeta": {
        "supports-color": {
          "optional": true
        }
      }
    },
    "node_modules/deep-is": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/deep-is/-/deep-is-0.1.4.tgz",
      "integrity": "sha512-oIPzksmTg4/MriiaYGO+okXDT7ztn/w3Eptv/+gSIdMdKsJo0u4CfYNFJPy+4SKMuCqGw2wxnA+URMg3t8a/bQ==",
      "dev": true
    },
    "node_modules/define-data-property": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/define-data-property/-/define-data-property-1.1.4.tgz",
      "integrity": "sha512-rBMvIzlpA8v6E+SJZoo++HAYqsLrkg7MSfIinMPFhmkorw7X+dOXVJQs+QT69zGkzMyfDnIMN2Wid1+NbL3T+A==",
      "dev": true,
      "dependencies": {
        "es-define-property": "^1.0.0",
        "es-errors": "^1.3.0",
        "gopd": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/define-properties": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/define-properties/-/define-properties-1.2.1.tgz",
      "integrity": "sha512-8QmQKqEASLd5nx0U1B1okLElbUuuttJ/AnYmRXbbbGDWh6uS208EjD4Xqq/I9wK7u0v6O08XhTWnt5XtEbR6Dg==",
      "dev": true,
      "dependencies": {
        "define-data-property": "^1.0.1",
        "has-property-descriptors": "^1.0.0",
        "object-keys": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/detect-libc": {
      "version": "2.1.2",
      "resolved": "https://registry.npmjs.org/detect-libc/-/detect-libc-2.1.2.tgz",
      "integrity": "sha512-Btj2BOOO83o3WyH59e8MgXsxEQVcarkUOpEYrubB0urwnN10yQ364rsiByU11nZlqWYZm05i/of7io4mzihBtQ==",
      "optional": true,
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/didyoumean": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/didyoumean/-/didyoumean-1.2.2.tgz",
      "integrity": "sha512-gxtyfqMg7GKyhQmb056K7M3xszy/myH8w+B4RT+QXBQsvAOdc3XymqDDPHx1BgPgsdAA5SIifona89YtRATDzw==",
      "dev": true
    },
    "node_modules/dlv": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/dlv/-/dlv-1.1.3.tgz",
      "integrity": "sha512-+HlytyjlPKnIG8XuRG8WvmBP8xs8P71y+SKKS6ZXWoEgLuePxtDoUEiH7WkdePWrQ5JBpE6aoVqfZfJUQkjXwA==",
      "dev": true
    },
    "node_modules/doctrine": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/doctrine/-/doctrine-2.1.0.tgz",
      "integrity": "sha512-35mSku4ZXK0vfCuHEDAwt55dg2jNajHZ1odvF+8SSr82EsZY4QmXfuWso8oEd8zRhVObSN18aM0CjSdoBX7zIw==",
      "dev": true,
      "dependencies": {
        "esutils": "^2.0.2"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/dunder-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/dunder-proto/-/dunder-proto-1.0.1.tgz",
      "integrity": "sha512-KIN/nDJBQRcXw0MLVhZE9iQHmG68qAVIBg9CqmUYjmQIhgij9U5MFvrqkUL5FbtyyzZuOeOt0zdeRe4UY7ct+A==",
      "dev": true,
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.1",
        "es-errors": "^1.3.0",
        "gopd": "^1.2.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/electron-to-chromium": {
      "version": "1.5.282",
      "resolved": "https://registry.npmjs.org/electron-to-chromium/-/electron-to-chromium-1.5.282.tgz",
      "integrity": "sha512-FCPkJtpst28UmFzd903iU7PdeVTfY0KAeJy+Lk0GLZRwgwYHn/irRcaCbQQOmr5Vytc/7rcavsYLvTM8RiHYhQ==",
      "dev": true
    },
    "node_modules/emoji-regex": {
      "version": "9.2.2",
      "resolved": "https://registry.npmjs.org/emoji-regex/-/emoji-regex-9.2.2.tgz",
      "integrity": "sha512-L18DaJsXSUk2+42pv8mLs5jJT2hqFkFE4j21wOmgbUqsZ2hL72NsUU785g9RXgo3s0ZNgVl42TiHp3ZtOv/Vyg==",
      "dev": true
    },
    "node_modules/es-abstract": {
      "version": "1.24.1",
      "resolved": "https://registry.npmjs.org/es-abstract/-/es-abstract-1.24.1.tgz",
      "integrity": "sha512-zHXBLhP+QehSSbsS9Pt23Gg964240DPd6QCf8WpkqEXxQ7fhdZzYsocOr5u7apWonsS5EjZDmTF+/slGMyasvw==",
      "dev": true,
      "dependencies": {
        "array-buffer-byte-length": "^1.0.2",
        "arraybuffer.prototype.slice": "^1.0.4",
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "data-view-buffer": "^1.0.2",
        "data-view-byte-length": "^1.0.2",
        "data-view-byte-offset": "^1.0.1",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "es-set-tostringtag": "^2.1.0",
        "es-to-primitive": "^1.3.0",
        "function.prototype.name": "^1.1.8",
        "get-intrinsic": "^1.3.0",
        "get-proto": "^1.0.1",
        "get-symbol-description": "^1.1.0",
        "globalthis": "^1.0.4",
        "gopd": "^1.2.0",
        "has-property-descriptors": "^1.0.2",
        "has-proto": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "internal-slot": "^1.1.0",
        "is-array-buffer": "^3.0.5",
        "is-callable": "^1.2.7",
        "is-data-view": "^1.0.2",
        "is-negative-zero": "^2.0.3",
        "is-regex": "^1.2.1",
        "is-set": "^2.0.3",
        "is-shared-array-buffer": "^1.0.4",
        "is-string": "^1.1.1",
        "is-typed-array": "^1.1.15",
        "is-weakref": "^1.1.1",
        "math-intrinsics": "^1.1.0",
        "object-inspect": "^1.13.4",
        "object-keys": "^1.1.1",
        "object.assign": "^4.1.7",
        "own-keys": "^1.0.1",
        "regexp.prototype.flags": "^1.5.4",
        "safe-array-concat": "^1.1.3",
        "safe-push-apply": "^1.0.0",
        "safe-regex-test": "^1.1.0",
        "set-proto": "^1.0.0",
        "stop-iteration-iterator": "^1.1.0",
        "string.prototype.trim": "^1.2.10",
        "string.prototype.trimend": "^1.0.9",
        "string.prototype.trimstart": "^1.0.8",
        "typed-array-buffer": "^1.0.3",
        "typed-array-byte-length": "^1.0.3",
        "typed-array-byte-offset": "^1.0.4",
        "typed-array-length": "^1.0.7",
        "unbox-primitive": "^1.1.0",
        "which-typed-array": "^1.1.19"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/es-define-property": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/es-define-property/-/es-define-property-1.0.1.tgz",
      "integrity": "sha512-e3nRfgfUZ4rNGL232gUgX06QNyyez04KdjFrF+LTRoOXmrOgFKDg4BCdsjW8EnT69eqdYGmRpJwiPVYNrCaW3g==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-errors": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-errors/-/es-errors-1.3.0.tgz",
      "integrity": "sha512-Zf5H2Kxt2xjTvbJvP2ZWLEICxA6j+hAmMzIlypy4xcBg1vKVnx89Wy0GbS+kf5cwCVFFzdCFh2XSCFNULS6csw==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-iterator-helpers": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/es-iterator-helpers/-/es-iterator-helpers-1.2.2.tgz",
      "integrity": "sha512-BrUQ0cPTB/IwXj23HtwHjS9n7O4h9FX94b4xc5zlTHxeLgTAdzYUDyy6KdExAl9lbN5rtfe44xpjpmj9grxs5w==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.24.1",
        "es-errors": "^1.3.0",
        "es-set-tostringtag": "^2.1.0",
        "function-bind": "^1.1.2",
        "get-intrinsic": "^1.3.0",
        "globalthis": "^1.0.4",
        "gopd": "^1.2.0",
        "has-property-descriptors": "^1.0.2",
        "has-proto": "^1.2.0",
        "has-symbols": "^1.1.0",
        "internal-slot": "^1.1.0",
        "iterator.prototype": "^1.1.5",
        "safe-array-concat": "^1.1.3"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-object-atoms": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/es-object-atoms/-/es-object-atoms-1.1.1.tgz",
      "integrity": "sha512-FGgH2h8zKNim9ljj7dankFPcICIK9Cp5bm+c2gQSYePhpaG5+esrLODihIorn+Pe6FGJzWhXQotPv73jTaldXA==",
      "dev": true,
      "dependencies": {
        "es-errors": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-set-tostringtag": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/es-set-tostringtag/-/es-set-tostringtag-2.1.0.tgz",
      "integrity": "sha512-j6vWzfrGVfyXxge+O0x5sh6cvxAog0a/4Rdd2K36zCMV5eJ+/+tOAngRO8cODMNWbVRdVlmGZQL2YS3yR8bIUA==",
      "dev": true,
      "dependencies": {
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6",
        "has-tostringtag": "^1.0.2",
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-shim-unscopables": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/es-shim-unscopables/-/es-shim-unscopables-1.1.0.tgz",
      "integrity": "sha512-d9T8ucsEhh8Bi1woXCf+TIKDIROLG5WCkxg8geBCbvk22kzwC5G2OnXVMO6FUsvQlgUUXQ2itephWDLqDzbeCw==",
      "dev": true,
      "dependencies": {
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-to-primitive": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-to-primitive/-/es-to-primitive-1.3.0.tgz",
      "integrity": "sha512-w+5mJ3GuFL+NjVtJlvydShqE1eN3h3PbI7/5LAsYJP/2qtuMXjfL2LpHSRqo4b4eSF5K/DH1JXKUAHSB2UW50g==",
      "dev": true,
      "dependencies": {
        "is-callable": "^1.2.7",
        "is-date-object": "^1.0.5",
        "is-symbol": "^1.0.4"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/escalade": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/escalade/-/escalade-3.2.0.tgz",
      "integrity": "sha512-WUj2qlxaQtO4g6Pq5c29GTcWGDyd8itL8zTlipgECz3JesAiiOKotd8JU6otB3PACgG6xkJUyVhboMS+bje/jA==",
      "dev": true,
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/escape-string-regexp": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-4.0.0.tgz",
      "integrity": "sha512-TtpcNJ3XAzx3Gq8sWRzJaVajRs0uVxA2YAkdb1jm2YkPz4G6egUFAyA3n5vtEIZefPk5Wa4UXbKuS5fKkJWdgA==",
      "dev": true,
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/eslint": {
      "version": "9.39.2",
      "resolved": "https://registry.npmjs.org/eslint/-/eslint-9.39.2.tgz",
      "integrity": "sha512-LEyamqS7W5HB3ujJyvi0HQK/dtVINZvd5mAAp9eT5S/ujByGjiZLCzPcHVzuXbpJDJF/cxwHlfceVUDZ2lnSTw==",
      "dev": true,
      "dependencies": {
        "@eslint-community/eslint-utils": "^4.8.0",
        "@eslint-community/regexpp": "^4.12.1",
        "@eslint/config-array": "^0.21.1",
        "@eslint/config-helpers": "^0.4.2",
        "@eslint/core": "^0.17.0",
        "@eslint/eslintrc": "^3.3.1",
        "@eslint/js": "9.39.2",
        "@eslint/plugin-kit": "^0.4.1",
        "@humanfs/node": "^0.16.6",
        "@humanwhocodes/module-importer": "^1.0.1",
        "@humanwhocodes/retry": "^0.4.2",
        "@types/estree": "^1.0.6",
        "ajv": "^6.12.4",
        "chalk": "^4.0.0",
        "cross-spawn": "^7.0.6",
        "debug": "^4.3.2",
        "escape-string-regexp": "^4.0.0",
        "eslint-scope": "^8.4.0",
        "eslint-visitor-keys": "^4.2.1",
        "espree": "^10.4.0",
        "esquery": "^1.5.0",
        "esutils": "^2.0.2",
        "fast-deep-equal": "^3.1.3",
        "file-entry-cache": "^8.0.0",
        "find-up": "^5.0.0",
        "glob-parent": "^6.0.2",
        "ignore": "^5.2.0",
        "imurmurhash": "^0.1.4",
        "is-glob": "^4.0.0",
        "json-stable-stringify-without-jsonify": "^1.0.1",
        "lodash.merge": "^4.6.2",
        "minimatch": "^3.1.2",
        "natural-compare": "^1.4.0",
        "optionator": "^0.9.3"
      },
      "bin": {
        "eslint": "bin/eslint.js"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "url": "https://eslint.org/donate"
      },
      "peerDependencies": {
        "jiti": "*"
      },
      "peerDependenciesMeta": {
        "jiti": {
          "optional": true
        }
      }
    },
    "node_modules/eslint-config-next": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/eslint-config-next/-/eslint-config-next-16.1.6.tgz",
      "integrity": "sha512-vKq40io2B0XtkkNDYyleATwblNt8xuh3FWp8SpSz3pt7P01OkBFlKsJZ2mWt5WsCySlDQLckb1zMY9yE9Qy0LA==",
      "dev": true,
      "dependencies": {
        "@next/eslint-plugin-next": "16.1.6",
        "eslint-import-resolver-node": "^0.3.6",
        "eslint-import-resolver-typescript": "^3.5.2",
        "eslint-plugin-import": "^2.32.0",
        "eslint-plugin-jsx-a11y": "^6.10.0",
        "eslint-plugin-react": "^7.37.0",
        "eslint-plugin-react-hooks": "^7.0.0",
        "globals": "16.4.0",
        "typescript-eslint": "^8.46.0"
      },
      "peerDependencies": {
        "eslint": ">=9.0.0",
        "typescript": ">=3.3.1"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/eslint-config-next/node_modules/globals": {
      "version": "16.4.0",
      "resolved": "https://registry.npmjs.org/globals/-/globals-16.4.0.tgz",
      "integrity": "sha512-ob/2LcVVaVGCYN+r14cnwnoDPUufjiYgSqRhiFD0Q1iI4Odora5RE8Iv1D24hAz5oMophRGkGz+yuvQmmUMnMw==",
      "dev": true,
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/eslint-import-resolver-node": {
      "version": "0.3.9",
      "resolved": "https://registry.npmjs.org/eslint-import-resolver-node/-/eslint-import-resolver-node-0.3.9.tgz",
      "integrity": "sha512-WFj2isz22JahUv+B788TlO3N6zL3nNJGU8CcZbPZvVEkBPaJdCV4vy5wyghty5ROFbCRnm132v8BScu5/1BQ8g==",
      "dev": true,
      "dependencies": {
        "debug": "^3.2.7",
        "is-core-module": "^2.13.0",
        "resolve": "^1.22.4"
      }
    },
    "node_modules/eslint-import-resolver-node/node_modules/debug": {
      "version": "3.2.7",
      "resolved": "https://registry.npmjs.org/debug/-/debug-3.2.7.tgz",
      "integrity": "sha512-CFjzYYAi4ThfiQvizrFQevTTXHtnCqWfe7x1AhgEscTz6ZbLbfoLRLPugTQyBth6f8ZERVUSyWHFD/7Wu4t1XQ==",
      "dev": true,
      "dependencies": {
        "ms": "^2.1.1"
      }
    },
    "node_modules/eslint-import-resolver-typescript": {
      "version": "3.10.1",
      "resolved": "https://registry.npmjs.org/eslint-import-resolver-typescript/-/eslint-import-resolver-typescript-3.10.1.tgz",
      "integrity": "sha512-A1rHYb06zjMGAxdLSkN2fXPBwuSaQ0iO5M/hdyS0Ajj1VBaRp0sPD3dn1FhME3c/JluGFbwSxyCfqdSbtQLAHQ==",
      "dev": true,
      "dependencies": {
        "@nolyfill/is-core-module": "1.0.39",
        "debug": "^4.4.0",
        "get-tsconfig": "^4.10.0",
        "is-bun-module": "^2.0.0",
        "stable-hash": "^0.0.5",
        "tinyglobby": "^0.2.13",
        "unrs-resolver": "^1.6.2"
      },
      "engines": {
        "node": "^14.18.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint-import-resolver-typescript"
      },
      "peerDependencies": {
        "eslint": "*",
        "eslint-plugin-import": "*",
        "eslint-plugin-import-x": "*"
      },
      "peerDependenciesMeta": {
        "eslint-plugin-import": {
          "optional": true
        },
        "eslint-plugin-import-x": {
          "optional": true
        }
      }
    },
    "node_modules/eslint-module-utils": {
      "version": "2.12.1",
      "resolved": "https://registry.npmjs.org/eslint-module-utils/-/eslint-module-utils-2.12.1.tgz",
      "integrity": "sha512-L8jSWTze7K2mTg0vos/RuLRS5soomksDPoJLXIslC7c8Wmut3bx7CPpJijDcBZtxQ5lrbUdM+s0OlNbz0DCDNw==",
      "dev": true,
      "dependencies": {
        "debug": "^3.2.7"
      },
      "engines": {
        "node": ">=4"
      },
      "peerDependenciesMeta": {
        "eslint": {
          "optional": true
        }
      }
    },
    "node_modules/eslint-module-utils/node_modules/debug": {
      "version": "3.2.7",
      "resolved": "https://registry.npmjs.org/debug/-/debug-3.2.7.tgz",
      "integrity": "sha512-CFjzYYAi4ThfiQvizrFQevTTXHtnCqWfe7x1AhgEscTz6ZbLbfoLRLPugTQyBth6f8ZERVUSyWHFD/7Wu4t1XQ==",
      "dev": true,
      "dependencies": {
        "ms": "^2.1.1"
      }
    },
    "node_modules/eslint-plugin-import": {
      "version": "2.32.0",
      "resolved": "https://registry.npmjs.org/eslint-plugin-import/-/eslint-plugin-import-2.32.0.tgz",
      "integrity": "sha512-whOE1HFo/qJDyX4SnXzP4N6zOWn79WhnCUY/iDR0mPfQZO8wcYE4JClzI2oZrhBnnMUCBCHZhO6VQyoBU95mZA==",
      "dev": true,
      "dependencies": {
        "@rtsao/scc": "^1.1.0",
        "array-includes": "^3.1.9",
        "array.prototype.findlastindex": "^1.2.6",
        "array.prototype.flat": "^1.3.3",
        "array.prototype.flatmap": "^1.3.3",
        "debug": "^3.2.7",
        "doctrine": "^2.1.0",
        "eslint-import-resolver-node": "^0.3.9",
        "eslint-module-utils": "^2.12.1",
        "hasown": "^2.0.2",
        "is-core-module": "^2.16.1",
        "is-glob": "^4.0.3",
        "minimatch": "^3.1.2",
        "object.fromentries": "^2.0.8",
        "object.groupby": "^1.0.3",
        "object.values": "^1.2.1",
        "semver": "^6.3.1",
        "string.prototype.trimend": "^1.0.9",
        "tsconfig-paths": "^3.15.0"
      },
      "engines": {
        "node": ">=4"
      },
      "peerDependencies": {
        "eslint": "^2 || ^3 || ^4 || ^5 || ^6 || ^7.2.0 || ^8 || ^9"
      }
    },
    "node_modules/eslint-plugin-import/node_modules/debug": {
      "version": "3.2.7",
      "resolved": "https://registry.npmjs.org/debug/-/debug-3.2.7.tgz",
      "integrity": "sha512-CFjzYYAi4ThfiQvizrFQevTTXHtnCqWfe7x1AhgEscTz6ZbLbfoLRLPugTQyBth6f8ZERVUSyWHFD/7Wu4t1XQ==",
      "dev": true,
      "dependencies": {
        "ms": "^2.1.1"
      }
    },
    "node_modules/eslint-plugin-jsx-a11y": {
      "version": "6.10.2",
      "resolved": "https://registry.npmjs.org/eslint-plugin-jsx-a11y/-/eslint-plugin-jsx-a11y-6.10.2.tgz",
      "integrity": "sha512-scB3nz4WmG75pV8+3eRUQOHZlNSUhFNq37xnpgRkCCELU3XMvXAxLk1eqWWyE22Ki4Q01Fnsw9BA3cJHDPgn2Q==",
      "dev": true,
      "dependencies": {
        "aria-query": "^5.3.2",
        "array-includes": "^3.1.8",
        "array.prototype.flatmap": "^1.3.2",
        "ast-types-flow": "^0.0.8",
        "axe-core": "^4.10.0",
        "axobject-query": "^4.1.0",
        "damerau-levenshtein": "^1.0.8",
        "emoji-regex": "^9.2.2",
        "hasown": "^2.0.2",
        "jsx-ast-utils": "^3.3.5",
        "language-tags": "^1.0.9",
        "minimatch": "^3.1.2",
        "object.fromentries": "^2.0.8",
        "safe-regex-test": "^1.0.3",
        "string.prototype.includes": "^2.0.1"
      },
      "engines": {
        "node": ">=4.0"
      },
      "peerDependencies": {
        "eslint": "^3 || ^4 || ^5 || ^6 || ^7 || ^8 || ^9"
      }
    },
    "node_modules/eslint-plugin-react": {
      "version": "7.37.5",
      "resolved": "https://registry.npmjs.org/eslint-plugin-react/-/eslint-plugin-react-7.37.5.tgz",
      "integrity": "sha512-Qteup0SqU15kdocexFNAJMvCJEfa2xUKNV4CC1xsVMrIIqEy3SQ/rqyxCWNzfrd3/ldy6HMlD2e0JDVpDg2qIA==",
      "dev": true,
      "dependencies": {
        "array-includes": "^3.1.8",
        "array.prototype.findlast": "^1.2.5",
        "array.prototype.flatmap": "^1.3.3",
        "array.prototype.tosorted": "^1.1.4",
        "doctrine": "^2.1.0",
        "es-iterator-helpers": "^1.2.1",
        "estraverse": "^5.3.0",
        "hasown": "^2.0.2",
        "jsx-ast-utils": "^2.4.1 || ^3.0.0",
        "minimatch": "^3.1.2",
        "object.entries": "^1.1.9",
        "object.fromentries": "^2.0.8",
        "object.values": "^1.2.1",
        "prop-types": "^15.8.1",
        "resolve": "^2.0.0-next.5",
        "semver": "^6.3.1",
        "string.prototype.matchall": "^4.0.12",
        "string.prototype.repeat": "^1.0.0"
      },
      "engines": {
        "node": ">=4"
      },
      "peerDependencies": {
        "eslint": "^3 || ^4 || ^5 || ^6 || ^7 || ^8 || ^9.7"
      }
    },
    "node_modules/eslint-plugin-react-hooks": {
      "version": "7.0.1",
      "resolved": "https://registry.npmjs.org/eslint-plugin-react-hooks/-/eslint-plugin-react-hooks-7.0.1.tgz",
      "integrity": "sha512-O0d0m04evaNzEPoSW+59Mezf8Qt0InfgGIBJnpC0h3NH/WjUAR7BIKUfysC6todmtiZ/A0oUVS8Gce0WhBrHsA==",
      "dev": true,
      "dependencies": {
        "@babel/core": "^7.24.4",
        "@babel/parser": "^7.24.4",
        "hermes-parser": "^0.25.1",
        "zod": "^3.25.0 || ^4.0.0",
        "zod-validation-error": "^3.5.0 || ^4.0.0"
      },
      "engines": {
        "node": ">=18"
      },
      "peerDependencies": {
        "eslint": "^3.0.0 || ^4.0.0 || ^5.0.0 || ^6.0.0 || ^7.0.0 || ^8.0.0-0 || ^9.0.0"
      }
    },
    "node_modules/eslint-plugin-react/node_modules/resolve": {
      "version": "2.0.0-next.5",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-2.0.0-next.5.tgz",
      "integrity": "sha512-U7WjGVG9sH8tvjW5SmGbQuui75FiyjAX72HX15DwBBwF9dNiQZRQAg9nnPhYy+TUnE0+VcrttuvNI8oSxZcocA==",
      "dev": true,
      "dependencies": {
        "is-core-module": "^2.13.0",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/eslint-scope": {
      "version": "8.4.0",
      "resolved": "https://registry.npmjs.org/eslint-scope/-/eslint-scope-8.4.0.tgz",
      "integrity": "sha512-sNXOfKCn74rt8RICKMvJS7XKV/Xk9kA7DyJr8mJik3S7Cwgy3qlkkmyS2uQB3jiJg6VNdZd/pDBJu0nvG2NlTg==",
      "dev": true,
      "dependencies": {
        "esrecurse": "^4.3.0",
        "estraverse": "^5.2.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/eslint-visitor-keys": {
      "version": "4.2.1",
      "resolved": "https://registry.npmjs.org/eslint-visitor-keys/-/eslint-visitor-keys-4.2.1.tgz",
      "integrity": "sha512-Uhdk5sfqcee/9H/rCOJikYz67o0a2Tw2hGRPOG2Y1R2dg7brRe1uG0yaNQDHu+TO/uQPF/5eCapvYSmHUjt7JQ==",
      "dev": true,
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/espree": {
      "version": "10.4.0",
      "resolved": "https://registry.npmjs.org/espree/-/espree-10.4.0.tgz",
      "integrity": "sha512-j6PAQ2uUr79PZhBjP5C5fhl8e39FmRnOjsD5lGnWrFU8i2G776tBK7+nP8KuQUTTyAZUwfQqXAgrVH5MbH9CYQ==",
      "dev": true,
      "dependencies": {
        "acorn": "^8.15.0",
        "acorn-jsx": "^5.3.2",
        "eslint-visitor-keys": "^4.2.1"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/esquery": {
      "version": "1.7.0",
      "resolved": "https://registry.npmjs.org/esquery/-/esquery-1.7.0.tgz",
      "integrity": "sha512-Ap6G0WQwcU/LHsvLwON1fAQX9Zp0A2Y6Y/cJBl9r/JbW90Zyg4/zbG6zzKa2OTALELarYHmKu0GhpM5EO+7T0g==",
      "dev": true,
      "dependencies": {
        "estraverse": "^5.1.0"
      },
      "engines": {
        "node": ">=0.10"
      }
    },
    "node_modules/esrecurse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/esrecurse/-/esrecurse-4.3.0.tgz",
      "integrity": "sha512-KmfKL3b6G+RXvP8N1vr3Tq1kL/oCFgn2NYXEtqP8/L3pKapUA4G8cFVaoF3SU323CD4XypR/ffioHmkti6/Tag==",
      "dev": true,
      "dependencies": {
        "estraverse": "^5.2.0"
      },
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/estraverse": {
      "version": "5.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-5.3.0.tgz",
      "integrity": "sha512-MMdARuVEQziNTeJD8DgMqmhwR11BRQ/cBP+pLtYdSTnf3MIO8fFeiINEbX36ZdNlfU/7A9f3gUw49B3oQsvwBA==",
      "dev": true,
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/esutils": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/esutils/-/esutils-2.0.3.tgz",
      "integrity": "sha512-kVscqXk4OCp68SZ0dkgEKVi6/8ij300KBWTJq32P/dYeWTSwK41WyTxalN1eRmA5Z9UU/LX9D7FWSmV9SAYx6g==",
      "dev": true,
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/fast-deep-equal": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/fast-deep-equal/-/fast-deep-equal-3.1.3.tgz",
      "integrity": "sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q==",
      "dev": true
    },
    "node_modules/fast-glob": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/fast-glob/-/fast-glob-3.3.1.tgz",
      "integrity": "sha512-kNFPyjhh5cKjrUltxs+wFx+ZkbRaxxmZ+X0ZU31SOsxCEtP9VPgtq2teZw1DebupL5GmDaNQ6yKMMVcM41iqDg==",
      "dev": true,
      "dependencies": {
        "@nodelib/fs.stat": "^2.0.2",
        "@nodelib/fs.walk": "^1.2.3",
        "glob-parent": "^5.1.2",
        "merge2": "^1.3.0",
        "micromatch": "^4.0.4"
      },
      "engines": {
        "node": ">=8.6.0"
      }
    },
    "node_modules/fast-glob/node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "dev": true,
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/fast-json-stable-stringify": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/fast-json-stable-stringify/-/fast-json-stable-stringify-2.1.0.tgz",
      "integrity": "sha512-lhd/wF+Lk98HZoTCtlVraHtfh5XYijIjalXck7saUtuanSDyLMxnHhSXEDJqHxD7msR8D0uCmqlkwjCV8xvwHw==",
      "dev": true
    },
    "node_modules/fast-levenshtein": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/fast-levenshtein/-/fast-levenshtein-2.0.6.tgz",
      "integrity": "sha512-DCXu6Ifhqcks7TZKY3Hxp3y6qphY5SJZmrWMDrKcERSOXWQdMhU9Ig/PYrzyw/ul9jOIyh0N4M0tbC5hodg8dw==",
      "dev": true
    },
    "node_modules/fastq": {
      "version": "1.20.1",
      "resolved": "https://registry.npmjs.org/fastq/-/fastq-1.20.1.tgz",
      "integrity": "sha512-GGToxJ/w1x32s/D2EKND7kTil4n8OVk/9mycTc4VDza13lOvpUZTGX3mFSCtV9ksdGBVzvsyAVLM6mHFThxXxw==",
      "dev": true,
      "dependencies": {
        "reusify": "^1.0.4"
      }
    },
    "node_modules/file-entry-cache": {
      "version": "8.0.0",
      "resolved": "https://registry.npmjs.org/file-entry-cache/-/file-entry-cache-8.0.0.tgz",
      "integrity": "sha512-XXTUwCvisa5oacNGRP9SfNtYBNAMi+RPwBFmblZEF7N7swHYQS6/Zfk7SRwx4D5j3CH211YNRco1DEMNVfZCnQ==",
      "dev": true,
      "dependencies": {
        "flat-cache": "^4.0.0"
      },
      "engines": {
        "node": ">=16.0.0"
      }
    },
    "node_modules/fill-range": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/fill-range/-/fill-range-7.1.1.tgz",
      "integrity": "sha512-YsGpe3WHLK8ZYi4tWDg2Jy3ebRz2rXowDxnld4bkQB00cc/1Zw9AWnC0i9ztDJitivtQvaI9KaLyKrc+hBW0yg==",
      "dev": true,
      "dependencies": {
        "to-regex-range": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/find-up": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-5.0.0.tgz",
      "integrity": "sha512-78/PXT1wlLLDgTzDs7sjq9hzz0vXD+zn+7wypEe4fXQxCmdmqfGsEPQxmiCSQI3ajFV91bVSsvNtrJRiW6nGng==",
      "dev": true,
      "dependencies": {
        "locate-path": "^6.0.0",
        "path-exists": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/flat-cache": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/flat-cache/-/flat-cache-4.0.1.tgz",
      "integrity": "sha512-f7ccFPK3SXFHpx15UIGyRJ/FJQctuKZ0zVuN3frBo4HnK3cay9VEW0R6yPYFHC0AgqhukPzKjq22t5DmAyqGyw==",
      "dev": true,
      "dependencies": {
        "flatted": "^3.2.9",
        "keyv": "^4.5.4"
      },
      "engines": {
        "node": ">=16"
      }
    },
    "node_modules/flatted": {
      "version": "3.3.3",
      "resolved": "https://registry.npmjs.org/flatted/-/flatted-3.3.3.tgz",
      "integrity": "sha512-GX+ysw4PBCz0PzosHDepZGANEuFCMLrnRTiEy9McGjmkCQYwRq4A/X786G/fjM/+OjsWSU1ZrY5qyARZmO/uwg==",
      "dev": true
    },
    "node_modules/for-each": {
      "version": "0.3.5",
      "resolved": "https://registry.npmjs.org/for-each/-/for-each-0.3.5.tgz",
      "integrity": "sha512-dKx12eRCVIzqCxFGplyFKJMPvLEWgmNtUrpTiJIR5u97zEhRG8ySrtboPHZXx7daLxQVrl643cTzbab2tkQjxg==",
      "dev": true,
      "dependencies": {
        "is-callable": "^1.2.7"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/fraction.js": {
      "version": "5.3.4",
      "resolved": "https://registry.npmjs.org/fraction.js/-/fraction.js-5.3.4.tgz",
      "integrity": "sha512-1X1NTtiJphryn/uLQz3whtY6jK3fTqoE3ohKs0tT+Ujr1W59oopxmoEh7Lu5p6vBaPbgoM0bzveAW4Qi5RyWDQ==",
      "dev": true,
      "engines": {
        "node": "*"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/rawify"
      }
    },
    "node_modules/fsevents": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.3.tgz",
      "integrity": "sha512-5xoDfX+fL7faATnagmWPpbFtwh/R77WmMMqqHGS65C3vvB0YHrgF+B1YmZ3441tMj5n63k0212XNoJwzlhffQw==",
      "dev": true,
      "hasInstallScript": true,
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/function-bind": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/function-bind/-/function-bind-1.1.2.tgz",
      "integrity": "sha512-7XHNxH7qX9xG5mIwxkhumTox/MIRNcOgDrxWsMt2pAr23WHp6MrRlN7FBSFpCpr+oVO0F744iUgR82nJMfG2SA==",
      "dev": true,
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/function.prototype.name": {
      "version": "1.1.8",
      "resolved": "https://registry.npmjs.org/function.prototype.name/-/function.prototype.name-1.1.8.tgz",
      "integrity": "sha512-e5iwyodOHhbMr/yNrc7fDYG4qlbIvI5gajyzPnb5TCwyhjApznQh1BMFou9b30SevY43gCJKXycoCBjMbsuW0Q==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "functions-have-names": "^1.2.3",
        "hasown": "^2.0.2",
        "is-callable": "^1.2.7"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/functions-have-names": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/functions-have-names/-/functions-have-names-1.2.3.tgz",
      "integrity": "sha512-xckBUXyTIqT97tq2x2AMb+g163b5JFysYk0x4qxNFwbfQkmNZoiRHb6sPzI9/QV33WeuvVYBUIiD4NzNIyqaRQ==",
      "dev": true,
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/generator-function": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/generator-function/-/generator-function-2.0.1.tgz",
      "integrity": "sha512-SFdFmIJi+ybC0vjlHN0ZGVGHc3lgE0DxPAT0djjVg+kjOnSqclqmj0KQ7ykTOLP6YxoqOvuAODGdcHJn+43q3g==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/gensync": {
      "version": "1.0.0-beta.2",
      "resolved": "https://registry.npmjs.org/gensync/-/gensync-1.0.0-beta.2.tgz",
      "integrity": "sha512-3hN7NaskYvMDLQY55gnW3NQ+mesEAepTqlg+VEbj7zzqEMBVNhzcGYYeqFo/TlYz6eQiFcp1HcsCZO+nGgS8zg==",
      "dev": true,
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/get-intrinsic": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/get-intrinsic/-/get-intrinsic-1.3.0.tgz",
      "integrity": "sha512-9fSjSaos/fRIVIp+xSJlE6lfwhES7LNtKaCBIamHsjr2na1BiABJPo0mOjjz8GJDURarmCPGqaiVg5mfjb98CQ==",
      "dev": true,
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "function-bind": "^1.1.2",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/get-proto/-/get-proto-1.0.1.tgz",
      "integrity": "sha512-sTSfBjoXBp89JvIKIefqw7U2CCebsc74kiY6awiGogKtoSGbgjYE/G/+l9sF3MWFPNc9IcoOC4ODfKHfxFmp0g==",
      "dev": true,
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/get-symbol-description": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/get-symbol-description/-/get-symbol-description-1.1.0.tgz",
      "integrity": "sha512-w9UMqWwJxHNOvoNzSJ2oPF5wvYcvP7jUvYzhp67yEhTi17ZDBBC1z9pTdGuzjD+EFIqLSYRweZjqfiPzQ06Ebg==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-tsconfig": {
      "version": "4.13.0",
      "resolved": "https://registry.npmjs.org/get-tsconfig/-/get-tsconfig-4.13.0.tgz",
      "integrity": "sha512-1VKTZJCwBrvbd+Wn3AOgQP/2Av+TfTCOlE4AcRJE72W1ksZXbAx8PPBR9RzgTeSPzlPMHrbANMH3LbltH73wxQ==",
      "dev": true,
      "dependencies": {
        "resolve-pkg-maps": "^1.0.0"
      },
      "funding": {
        "url": "https://github.com/privatenumber/get-tsconfig?sponsor=1"
      }
    },
    "node_modules/glob-parent": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-6.0.2.tgz",
      "integrity": "sha512-XxwI8EOhVQgWp6iDL+3b0r86f4d6AX6zSU55HfB4ydCEuXLXc5FcYeOu+nnGftS4TEju/11rt4KJPTMgbfmv4A==",
      "dev": true,
      "dependencies": {
        "is-glob": "^4.0.3"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/globals": {
      "version": "14.0.0",
      "resolved": "https://registry.npmjs.org/globals/-/globals-14.0.0.tgz",
      "integrity": "sha512-oahGvuMGQlPw/ivIYBjVSrWAfWLBeku5tpPE2fOPLi+WHffIWbuh2tCjhyQhTBPMf5E9jDEH4FOmTYgYwbKwtQ==",
      "dev": true,
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/globalthis": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/globalthis/-/globalthis-1.0.4.tgz",
      "integrity": "sha512-DpLKbNU4WylpxJykQujfCcwYWiV/Jhm50Goo0wrVILAv5jOr9d+H+UR3PhSCD2rCCEIg0uc+G+muBTwD54JhDQ==",
      "dev": true,
      "dependencies": {
        "define-properties": "^1.2.1",
        "gopd": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/gopd": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/gopd/-/gopd-1.2.0.tgz",
      "integrity": "sha512-ZUKRh6/kUFoAiTAtTYPZJ3hw9wNxx+BIBOijnlG9PnrJsCcSjs1wyyD6vJpaYtgnzDrKYRSqf3OO6Rfa93xsRg==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-bigints": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-bigints/-/has-bigints-1.1.0.tgz",
      "integrity": "sha512-R3pbpkcIqv2Pm3dUwgjclDRVmWpTJW2DcMzcIhEXEx1oh/CEMObMm3KLmRJOdvhM7o4uQBnwr8pzRK2sJWIqfg==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-flag": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/has-flag/-/has-flag-4.0.0.tgz",
      "integrity": "sha512-EykJT/Q1KjTWctppgIAgfSO0tKVuZUjhgMr17kqTumMl6Afv3EISleU7qZUzoXDFTAHTDC4NOoG/ZxU3EvlMPQ==",
      "dev": true,
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/has-property-descriptors": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/has-property-descriptors/-/has-property-descriptors-1.0.2.tgz",
      "integrity": "sha512-55JNKuIW+vq4Ke1BjOTjM2YctQIvCT7GFzHwmfZPGo5wnrgkid0YQtnAleFSqumZm4az3n2BS+erby5ipJdgrg==",
      "dev": true,
      "dependencies": {
        "es-define-property": "^1.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-proto": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/has-proto/-/has-proto-1.2.0.tgz",
      "integrity": "sha512-KIL7eQPfHQRC8+XluaIw7BHUwwqL19bQn4hzNgdr+1wXoU0KKj6rufu47lhY7KbJR2C6T6+PfyN0Ea7wkSS+qQ==",
      "dev": true,
      "dependencies": {
        "dunder-proto": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-symbols": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-symbols/-/has-symbols-1.1.0.tgz",
      "integrity": "sha512-1cDNdwJ2Jaohmb3sg4OmKaMBwuC48sYni5HUw2DvsC8LjGTLK9h+eb1X6RyuOHe4hT0ULCW68iomhjUoKUqlPQ==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-tostringtag": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/has-tostringtag/-/has-tostringtag-1.0.2.tgz",
      "integrity": "sha512-NqADB8VjPFLM2V0VvHUewwwsw0ZWBaIdgo+ieHtK3hasLz4qeCRjYcqfB6AQrBggRKppKF8L52/VqdVsO47Dlw==",
      "dev": true,
      "dependencies": {
        "has-symbols": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/hasown": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/hasown/-/hasown-2.0.2.tgz",
      "integrity": "sha512-0hJU9SCPvmMzIBdZFqNPXWa6dqh7WdH0cII9y+CyS8rG3nL48Bclra9HmKhVVUHyPWNH5Y7xDwAB7bfgSjkUMQ==",
      "dev": true,
      "dependencies": {
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/hermes-estree": {
      "version": "0.25.1",
      "resolved": "https://registry.npmjs.org/hermes-estree/-/hermes-estree-0.25.1.tgz",
      "integrity": "sha512-0wUoCcLp+5Ev5pDW2OriHC2MJCbwLwuRx+gAqMTOkGKJJiBCLjtrvy4PWUGn6MIVefecRpzoOZ/UV6iGdOr+Cw==",
      "dev": true
    },
    "node_modules/hermes-parser": {
      "version": "0.25.1",
      "resolved": "https://registry.npmjs.org/hermes-parser/-/hermes-parser-0.25.1.tgz",
      "integrity": "sha512-6pEjquH3rqaI6cYAXYPcz9MS4rY6R4ngRgrgfDshRptUZIc3lw0MCIJIGDj9++mfySOuPTHB4nrSW99BCvOPIA==",
      "dev": true,
      "dependencies": {
        "hermes-estree": "0.25.1"
      }
    },
    "node_modules/ignore": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/ignore/-/ignore-5.3.2.tgz",
      "integrity": "sha512-hsBTNUqQTDwkWtcdYI2i06Y/nUBEsNEDJKjWdigLvegy8kDuJAS8uRlpkkcQpyEXL0Z/pjDy5HBmMjRCJ2gq+g==",
      "dev": true,
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/import-fresh": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/import-fresh/-/import-fresh-3.3.1.tgz",
      "integrity": "sha512-TR3KfrTZTYLPB6jUjfx6MF9WcWrHL9su5TObK4ZkYgBdWKPOFoSoQIdEuTuR82pmtxH2spWG9h6etwfr1pLBqQ==",
      "dev": true,
      "dependencies": {
        "parent-module": "^1.0.0",
        "resolve-from": "^4.0.0"
      },
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/imurmurhash": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/imurmurhash/-/imurmurhash-0.1.4.tgz",
      "integrity": "sha512-JmXMZ6wuvDmLiHEml9ykzqO6lwFbof0GG4IkcGaENdCRDDmMVnny7s5HsIgHCbaq0w2MyPhDqkhTUgS2LU2PHA==",
      "dev": true,
      "engines": {
        "node": ">=0.8.19"
      }
    },
    "node_modules/internal-slot": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/internal-slot/-/internal-slot-1.1.0.tgz",
      "integrity": "sha512-4gd7VpWNQNB4UKKCFFVcp1AVv+FMOgs9NKzjHKusc8jTMhd5eL1NqQqOpE0KzMds804/yHlglp3uxgluOqAPLw==",
      "dev": true,
      "dependencies": {
        "es-errors": "^1.3.0",
        "hasown": "^2.0.2",
        "side-channel": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/is-array-buffer": {
      "version": "3.0.5",
      "resolved": "https://registry.npmjs.org/is-array-buffer/-/is-array-buffer-3.0.5.tgz",
      "integrity": "sha512-DDfANUiiG2wC1qawP66qlTugJeL5HyzMpfr8lLK+jMQirGzNod0B12cFB/9q838Ru27sBwfw78/rdoU7RERz6A==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-async-function": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-async-function/-/is-async-function-2.1.1.tgz",
      "integrity": "sha512-9dgM/cZBnNvjzaMYHVoxxfPj2QXt22Ev7SuuPrs+xav0ukGB0S6d4ydZdEiM48kLx5kDV+QBPrpVnFyefL8kkQ==",
      "dev": true,
      "dependencies": {
        "async-function": "^1.0.0",
        "call-bound": "^1.0.3",
        "get-proto": "^1.0.1",
        "has-tostringtag": "^1.0.2",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-bigint": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/is-bigint/-/is-bigint-1.1.0.tgz",
      "integrity": "sha512-n4ZT37wG78iz03xPRKJrHTdZbe3IicyucEtdRsV5yglwc3GyUfbAfpSeD0FJ41NbUNSt5wbhqfp1fS+BgnvDFQ==",
      "dev": true,
      "dependencies": {
        "has-bigints": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-binary-path": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/is-binary-path/-/is-binary-path-2.1.0.tgz",
      "integrity": "sha512-ZMERYes6pDydyuGidse7OsHxtbI7WVeUEozgR/g7rd0xUimYNlvZRE/K2MgZTjWy725IfelLeVcEM97mmtRGXw==",
      "dev": true,
      "dependencies": {
        "binary-extensions": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-boolean-object": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/is-boolean-object/-/is-boolean-object-1.2.2.tgz",
      "integrity": "sha512-wa56o2/ElJMYqjCjGkXri7it5FbebW5usLw/nPmCMs5DeZ7eziSYZhSmPRn0txqeW4LnAmQQU7FgqLpsEFKM4A==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-bun-module": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/is-bun-module/-/is-bun-module-2.0.0.tgz",
      "integrity": "sha512-gNCGbnnnnFAUGKeZ9PdbyeGYJqewpmc2aKHUEMO5nQPWU9lOmv7jcmQIv+qHD8fXW6W7qfuCwX4rY9LNRjXrkQ==",
      "dev": true,
      "dependencies": {
        "semver": "^7.7.1"
      }
    },
    "node_modules/is-bun-module/node_modules/semver": {
      "version": "7.7.3",
      "resolved": "https://registry.npmjs.org/semver/-/semver-7.7.3.tgz",
      "integrity": "sha512-SdsKMrI9TdgjdweUSR9MweHA4EJ8YxHn8DFaDisvhVlUOe4BF1tLD7GAj0lIqWVl+dPb/rExr0Btby5loQm20Q==",
      "dev": true,
      "bin": {
        "semver": "bin/semver.js"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/is-callable": {
      "version": "1.2.7",
      "resolved": "https://registry.npmjs.org/is-callable/-/is-callable-1.2.7.tgz",
      "integrity": "sha512-1BC0BVFhS/p0qtw6enp8e+8OD0UrK0oFLztSjNzhcKA3WDuJxxAPXzPuPtKkjEY9UUoEWlX/8fgKeu2S8i9JTA==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-core-module": {
      "version": "2.16.1",
      "resolved": "https://registry.npmjs.org/is-core-module/-/is-core-module-2.16.1.tgz",
      "integrity": "sha512-UfoeMA6fIJ8wTYFEUjelnaGI67v6+N7qXJEvQuIGa99l4xsCruSYOVSQ0uPANn4dAzm8lkYPaKLrrijLq7x23w==",
      "dev": true,
      "dependencies": {
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-data-view": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/is-data-view/-/is-data-view-1.0.2.tgz",
      "integrity": "sha512-RKtWF8pGmS87i2D6gqQu/l7EYRlVdfzemCJN/P3UOs//x1QE7mfhvzHIApBTRf7axvT6DMGwSwBXYCT0nfB9xw==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.2",
        "get-intrinsic": "^1.2.6",
        "is-typed-array": "^1.1.13"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-date-object": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/is-date-object/-/is-date-object-1.1.0.tgz",
      "integrity": "sha512-PwwhEakHVKTdRNVOw+/Gyh0+MzlCl4R6qKvkhuvLtPMggI1WAHt9sOwZxQLSGpUaDnrdyDsomoRgNnCfKNSXXg==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.2",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-extglob": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-extglob/-/is-extglob-2.1.1.tgz",
      "integrity": "sha512-SbKbANkN603Vi4jEZv49LeVJMn4yGwsbzZworEoyEiutsN3nJYdbO36zfhGJ6QEDpOZIFkDtnq5JRxmvl3jsoQ==",
      "dev": true,
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-finalizationregistry": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-finalizationregistry/-/is-finalizationregistry-1.1.1.tgz",
      "integrity": "sha512-1pC6N8qWJbWoPtEjgcL2xyhQOP491EQjeUo3qTKcmV8YSDDJrOepfG8pcC7h/QgnQHYSv0mJ3Z/ZWxmatVrysg==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-generator-function": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/is-generator-function/-/is-generator-function-1.1.2.tgz",
      "integrity": "sha512-upqt1SkGkODW9tsGNG5mtXTXtECizwtS2kA161M+gJPc1xdb/Ax629af6YrTwcOeQHbewrPNlE5Dx7kzvXTizA==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.4",
        "generator-function": "^2.0.0",
        "get-proto": "^1.0.1",
        "has-tostringtag": "^1.0.2",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-glob": {
      "version": "4.0.3",
      "resolved": "https://registry.npmjs.org/is-glob/-/is-glob-4.0.3.tgz",
      "integrity": "sha512-xelSayHH36ZgE7ZWhli7pW34hNbNl8Ojv5KVmkJD4hBdD3th8Tfk9vYasLM+mXWOZhFkgZfxhLSnrwRr4elSSg==",
      "dev": true,
      "dependencies": {
        "is-extglob": "^2.1.1"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-map": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-map/-/is-map-2.0.3.tgz",
      "integrity": "sha512-1Qed0/Hr2m+YqxnM09CjA2d/i6YZNfF6R2oRAOj36eUdS6qIV/huPJNSEpKbupewFs+ZsJlxsjjPbc0/afW6Lw==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-negative-zero": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-negative-zero/-/is-negative-zero-2.0.3.tgz",
      "integrity": "sha512-5KoIu2Ngpyek75jXodFvnafB6DJgr3u8uuK0LEZJjrU19DrMD3EVERaR8sjz8CCGgpZvxPl9SuE1GMVPFHx1mw==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-number": {
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/is-number/-/is-number-7.0.0.tgz",
      "integrity": "sha512-41Cifkg6e8TylSpdtTpeLVMqvSBEVzTttHvERD741+pnZ8ANv0004MRL43QKPDlK9cGvNp6NZWZUBlbGXYxxng==",
      "dev": true,
      "engines": {
        "node": ">=0.12.0"
      }
    },
    "node_modules/is-number-object": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-number-object/-/is-number-object-1.1.1.tgz",
      "integrity": "sha512-lZhclumE1G6VYD8VHe35wFaIif+CTy5SJIi5+3y4psDgWu4wPDoBhF8NxUOinEc7pHgiTsT6MaBb92rKhhD+Xw==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-regex": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/is-regex/-/is-regex-1.2.1.tgz",
      "integrity": "sha512-MjYsKHO5O7mCsmRGxWcLWheFqN9DJ/2TmngvjKXihe6efViPqc274+Fx/4fYj/r03+ESvBdTXK0V6tA3rgez1g==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.2",
        "gopd": "^1.2.0",
        "has-tostringtag": "^1.0.2",
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-set": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-set/-/is-set-2.0.3.tgz",
      "integrity": "sha512-iPAjerrse27/ygGLxw+EBR9agv9Y6uLeYVJMu+QNCoouJ1/1ri0mGrcWpfCqFZuzzx3WjtwxG098X+n4OuRkPg==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-shared-array-buffer": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/is-shared-array-buffer/-/is-shared-array-buffer-1.0.4.tgz",
      "integrity": "sha512-ISWac8drv4ZGfwKl5slpHG9OwPNty4jOWPRIhBpxOoD+hqITiwuipOQ2bNthAzwA3B4fIjO4Nln74N0S9byq8A==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-string": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-string/-/is-string-1.1.1.tgz",
      "integrity": "sha512-BtEeSsoaQjlSPBemMQIrY1MY0uM6vnS1g5fmufYOtnxLGUZM2178PKbhsk7Ffv58IX+ZtcvoGwccYsh0PglkAA==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-symbol": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-symbol/-/is-symbol-1.1.1.tgz",
      "integrity": "sha512-9gGx6GTtCQM73BgmHQXfDmLtfjjTUDSyoxTCbp5WtoixAhfgsDirWIcVQ/IHpvI5Vgd5i/J5F7B9cN/WlVbC/w==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.2",
        "has-symbols": "^1.1.0",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-typed-array": {
      "version": "1.1.15",
      "resolved": "https://registry.npmjs.org/is-typed-array/-/is-typed-array-1.1.15.tgz",
      "integrity": "sha512-p3EcsicXjit7SaskXHs1hA91QxgTw46Fv6EFKKGS5DRFLD8yKnohjF3hxoju94b/OcMZoQukzpPpBE9uLVKzgQ==",
      "dev": true,
      "dependencies": {
        "which-typed-array": "^1.1.16"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-weakmap": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/is-weakmap/-/is-weakmap-2.0.2.tgz",
      "integrity": "sha512-K5pXYOm9wqY1RgjpL3YTkF39tni1XajUIkawTLUo9EZEVUFga5gSQJF8nNS7ZwJQ02y+1YCNYcMh+HIf1ZqE+w==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-weakref": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-weakref/-/is-weakref-1.1.1.tgz",
      "integrity": "sha512-6i9mGWSlqzNMEqpCp93KwRS1uUOodk2OJ6b+sq7ZPDSy2WuI5NFIxp/254TytR8ftefexkWn5xNiHUNpPOfSew==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-weakset": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/is-weakset/-/is-weakset-2.0.4.tgz",
      "integrity": "sha512-mfcwb6IzQyOKTs84CQMrOwW4gQcaTOAWJ0zzJCl2WSPDrWk/OzDaImWFH3djXhb24g4eudZfLRozAvPGw4d9hQ==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/isarray": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/isarray/-/isarray-2.0.5.tgz",
      "integrity": "sha512-xHjhDr3cNBK0BzdUJSPXZntQUx/mwMS5Rw4A7lPJ90XGAO6ISP/ePDNuo0vhqOZU+UD5JoodwCAAoZQd3FeAKw==",
      "dev": true
    },
    "node_modules/isexe": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/isexe/-/isexe-2.0.0.tgz",
      "integrity": "sha512-RHxMLp9lnKHGHRng9QFhRCMbYAcVpn69smSGcq3f36xjgVVWThj4qqLbTLlq7Ssj8B+fIQ1EuCEGI2lKsyQeIw==",
      "dev": true
    },
    "node_modules/iterator.prototype": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/iterator.prototype/-/iterator.prototype-1.1.5.tgz",
      "integrity": "sha512-H0dkQoCa3b2VEeKQBOxFph+JAbcrQdE7KC0UkqwpLmv2EC4P41QXP+rqo9wYodACiG5/WM5s9oDApTU8utwj9g==",
      "dev": true,
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.6",
        "get-proto": "^1.0.0",
        "has-symbols": "^1.1.0",
        "set-function-name": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/jiti": {
      "version": "1.21.7",
      "resolved": "https://registry.npmjs.org/jiti/-/jiti-1.21.7.tgz",
      "integrity": "sha512-/imKNG4EbWNrVjoNC/1H5/9GFy+tqjGBHCaSsN+P2RnPqjsLmv6UD3Ej+Kj8nBWaRAwyk7kK5ZUc+OEatnTR3A==",
      "dev": true,
      "bin": {
        "jiti": "bin/jiti.js"
      }
    },
    "node_modules/js-tokens": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/js-tokens/-/js-tokens-4.0.0.tgz",
      "integrity": "sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ==",
      "dev": true
    },
    "node_modules/js-yaml": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/js-yaml/-/js-yaml-4.1.1.tgz",
      "integrity": "sha512-qQKT4zQxXl8lLwBtHMWwaTcGfFOZviOJet3Oy/xmGk2gZH677CJM9EvtfdSkgWcATZhj/55JZ0rmy3myCT5lsA==",
      "dev": true,
      "dependencies": {
        "argparse": "^2.0.1"
      },
      "bin": {
        "js-yaml": "bin/js-yaml.js"
      }
    },
    "node_modules/jsesc": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/jsesc/-/jsesc-3.1.0.tgz",
      "integrity": "sha512-/sM3dO2FOzXjKQhJuo0Q173wf2KOo8t4I8vHy6lF9poUp7bKT0/NHE8fPX23PwfhnykfqnC2xRxOnVw5XuGIaA==",
      "dev": true,
      "bin": {
        "jsesc": "bin/jsesc"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/json-buffer": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/json-buffer/-/json-buffer-3.0.1.tgz",
      "integrity": "sha512-4bV5BfR2mqfQTJm+V5tPPdf+ZpuhiIvTuAB5g8kcrXOZpTT/QwwVRWBywX1ozr6lEuPdbHxwaJlm9G6mI2sfSQ==",
      "dev": true
    },
    "node_modules/json-schema-traverse": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-0.4.1.tgz",
      "integrity": "sha512-xbbCH5dCYU5T8LcEhhuh7HJ88HXuW3qsI3Y0zOZFKfZEHcpWiHU/Jxzk629Brsab/mMiHQti9wMP+845RPe3Vg==",
      "dev": true
    },
    "node_modules/json-stable-stringify-without-jsonify": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/json-stable-stringify-without-jsonify/-/json-stable-stringify-without-jsonify-1.0.1.tgz",
      "integrity": "sha512-Bdboy+l7tA3OGW6FjyFHWkP5LuByj1Tk33Ljyq0axyzdk9//JSi2u3fP1QSmd1KNwq6VOKYGlAu87CisVir6Pw==",
      "dev": true
    },
    "node_modules/json5": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/json5/-/json5-2.2.3.tgz",
      "integrity": "sha512-XmOWe7eyHYH14cLdVPoyg+GOH3rYX++KpzrylJwSW98t3Nk+U8XOl8FWKOgwtzdb8lXGf6zYwDUzeHMWfxasyg==",
      "dev": true,
      "bin": {
        "json5": "lib/cli.js"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/jsx-ast-utils": {
      "version": "3.3.5",
      "resolved": "https://registry.npmjs.org/jsx-ast-utils/-/jsx-ast-utils-3.3.5.tgz",
      "integrity": "sha512-ZZow9HBI5O6EPgSJLUb8n2NKgmVWTwCvHGwFuJlMjvLFqlGG6pjirPhtdsseaLZjSibD8eegzmYpUZwoIlj2cQ==",
      "dev": true,
      "dependencies": {
        "array-includes": "^3.1.6",
        "array.prototype.flat": "^1.3.1",
        "object.assign": "^4.1.4",
        "object.values": "^1.1.6"
      },
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/keyv": {
      "version": "4.5.4",
      "resolved": "https://registry.npmjs.org/keyv/-/keyv-4.5.4.tgz",
      "integrity": "sha512-oxVHkHR/EJf2CNXnWxRLW6mg7JyCCUcG0DtEGmL2ctUo1PNTin1PUil+r/+4r5MpVgC/fn1kjsx7mjSujKqIpw==",
      "dev": true,
      "dependencies": {
        "json-buffer": "3.0.1"
      }
    },
    "node_modules/language-subtag-registry": {
      "version": "0.3.23",
      "resolved": "https://registry.npmjs.org/language-subtag-registry/-/language-subtag-registry-0.3.23.tgz",
      "integrity": "sha512-0K65Lea881pHotoGEa5gDlMxt3pctLi2RplBb7Ezh4rRdLEOtgi7n4EwK9lamnUCkKBqaeKRVebTq6BAxSkpXQ==",
      "dev": true
    },
    "node_modules/language-tags": {
      "version": "1.0.9",
      "resolved": "https://registry.npmjs.org/language-tags/-/language-tags-1.0.9.tgz",
      "integrity": "sha512-MbjN408fEndfiQXbFQ1vnd+1NoLDsnQW41410oQBXiyXDMYH5z505juWa4KUE1LqxRC7DgOgZDbKLxHIwm27hA==",
      "dev": true,
      "dependencies": {
        "language-subtag-registry": "^0.3.20"
      },
      "engines": {
        "node": ">=0.10"
      }
    },
    "node_modules/levn": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/levn/-/levn-0.4.1.tgz",
      "integrity": "sha512-+bT2uH4E5LGE7h/n3evcS/sQlJXCpIp6ym8OWJ5eV6+67Dsql/LaaT7qJBAt2rzfoa/5QBGBhxDix1dMt2kQKQ==",
      "dev": true,
      "dependencies": {
        "prelude-ls": "^1.2.1",
        "type-check": "~0.4.0"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/lilconfig": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/lilconfig/-/lilconfig-3.1.3.tgz",
      "integrity": "sha512-/vlFKAoH5Cgt3Ie+JLhRbwOsCQePABiU3tJ1egGvyQ+33R/vcwM2Zl2QR/LzjsBeItPt3oSVXapn+m4nQDvpzw==",
      "dev": true,
      "engines": {
        "node": ">=14"
      },
      "funding": {
        "url": "https://github.com/sponsors/antonk52"
      }
    },
    "node_modules/lines-and-columns": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/lines-and-columns/-/lines-and-columns-1.2.4.tgz",
      "integrity": "sha512-7ylylesZQ/PV29jhEDl3Ufjo6ZX7gCqJr5F7PKrqc93v7fzSymt1BpwEU8nAUXs8qzzvqhbjhK5QZg6Mt/HkBg==",
      "dev": true
    },
    "node_modules/locate-path": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-6.0.0.tgz",
      "integrity": "sha512-iPZK6eYjbxRu3uB4/WZ3EsEIMJFMqAoopl3R+zuq0UjcAm/MO6KCweDgPfP3elTztoKP3KtnVHxTn2NHBSDVUw==",
      "dev": true,
      "dependencies": {
        "p-locate": "^5.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/lodash.merge": {
      "version": "4.6.2",
      "resolved": "https://registry.npmjs.org/lodash.merge/-/lodash.merge-4.6.2.tgz",
      "integrity": "sha512-0KpjqXRVvrYyCsX1swR/XTK0va6VQkQM6MNo7PqW77ByjAhoARA8EfrP1N4+KlKj8YS0ZUCtRT/YUuhyYDujIQ==",
      "dev": true
    },
    "node_modules/loose-envify": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/loose-envify/-/loose-envify-1.4.0.tgz",
      "integrity": "sha512-lyuxPGr/Wfhrlem2CL/UcnUc1zcqKAImBDzukY7Y5F/yQiNdko6+fRLevlw1HgMySw7f611UIY408EtxRSoK3Q==",
      "dev": true,
      "dependencies": {
        "js-tokens": "^3.0.0 || ^4.0.0"
      },
      "bin": {
        "loose-envify": "cli.js"
      }
    },
    "node_modules/lru-cache": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/lru-cache/-/lru-cache-5.1.1.tgz",
      "integrity": "sha512-KpNARQA3Iwv+jTA0utUVVbrh+Jlrr1Fv0e56GGzAFOXN7dk/FviaDW8LHmK52DlcH4WP2n6gI8vN1aesBFgo9w==",
      "dev": true,
      "dependencies": {
        "yallist": "^3.0.2"
      }
    },
    "node_modules/math-intrinsics": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/math-intrinsics/-/math-intrinsics-1.1.0.tgz",
      "integrity": "sha512-/IXtbwEk5HTPyEwyKX6hGkYXxM9nbj64B+ilVJnC/R6B0pH5G4V3b0pVbL7DBj4tkhBAppbQUlf6F6Xl9LHu1g==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/merge2": {
      "version": "1.4.1",
      "resolved": "https://registry.npmjs.org/merge2/-/merge2-1.4.1.tgz",
      "integrity": "sha512-8q7VEgMJW4J8tcfVPy8g09NcQwZdbwFEqhe/WZkoIzjn/3TGDwtOCYtXGxA3O8tPzpczCCDgv+P2P5y00ZJOOg==",
      "dev": true,
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/micromatch": {
      "version": "4.0.8",
      "resolved": "https://registry.npmjs.org/micromatch/-/micromatch-4.0.8.tgz",
      "integrity": "sha512-PXwfBhYu0hBCPw8Dn0E+WDYb7af3dSLVWKi3HGv84IdF4TyFoC0ysxFd0Goxw7nSv4T/PzEJQxsYsEiFCKo2BA==",
      "dev": true,
      "dependencies": {
        "braces": "^3.0.3",
        "picomatch": "^2.3.1"
      },
      "engines": {
        "node": ">=8.6"
      }
    },
    "node_modules/minimatch": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-3.1.2.tgz",
      "integrity": "sha512-J7p63hRiAjw1NDEww1W7i37+ByIrOWO5XQQAzZ3VOcL0PNybwpfmV/N05zFAzwQ9USyEcX6t3UO+K5aqBQOIHw==",
      "dev": true,
      "dependencies": {
        "brace-expansion": "^1.1.7"
      },
      "engines": {
        "node": "*"
      }
    },
    "node_modules/minimist": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/minimist/-/minimist-1.2.8.tgz",
      "integrity": "sha512-2yyAR8qBkN3YuheJanUpWC5U3bb5osDywNB8RzDVlDwDHbocAJveqqj1u8+SVD7jkWT4yvsHCpWqqWqAxb0zCA==",
      "dev": true,
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/ms": {
      "version": "2.1.3",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.1.3.tgz",
      "integrity": "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA==",
      "dev": true
    },
    "node_modules/mz": {
      "version": "2.7.0",
      "resolved": "https://registry.npmjs.org/mz/-/mz-2.7.0.tgz",
      "integrity": "sha512-z81GNO7nnYMEhrGh9LeymoE4+Yr0Wn5McHIZMK5cfQCl+NDX08sCZgUc9/6MHni9IWuFLm1Z3HTCXu2z9fN62Q==",
      "dev": true,
      "dependencies": {
        "any-promise": "^1.0.0",
        "object-assign": "^4.0.1",
        "thenify-all": "^1.0.0"
      }
    },
    "node_modules/nanoid": {
      "version": "3.3.11",
      "resolved": "https://registry.npmjs.org/nanoid/-/nanoid-3.3.11.tgz",
      "integrity": "sha512-N8SpfPUnUp1bK+PMYW8qSWdl9U+wwNWI4QKxOYDy9JAro3WMX7p2OeVRF9v+347pnakNevPmiHhNmZ2HbFA76w==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "bin": {
        "nanoid": "bin/nanoid.cjs"
      },
      "engines": {
        "node": "^10 || ^12 || ^13.7 || ^14 || >=15.0.1"
      }
    },
    "node_modules/napi-postinstall": {
      "version": "0.3.4",
      "resolved": "https://registry.npmjs.org/napi-postinstall/-/napi-postinstall-0.3.4.tgz",
      "integrity": "sha512-PHI5f1O0EP5xJ9gQmFGMS6IZcrVvTjpXjz7Na41gTE7eE2hK11lg04CECCYEEjdc17EV4DO+fkGEtt7TpTaTiQ==",
      "dev": true,
      "bin": {
        "napi-postinstall": "lib/cli.js"
      },
      "engines": {
        "node": "^12.20.0 || ^14.18.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/napi-postinstall"
      }
    },
    "node_modules/natural-compare": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/natural-compare/-/natural-compare-1.4.0.tgz",
      "integrity": "sha512-OWND8ei3VtNC9h7V60qff3SVobHr996CTwgxubgyQYEpg290h9J0buyECNNJexkFm5sOajh5G116RYA1c8ZMSw==",
      "dev": true
    },
    "node_modules/next": {
      "version": "16.1.6",
      "resolved": "https://registry.npmjs.org/next/-/next-16.1.6.tgz",
      "integrity": "sha512-hkyRkcu5x/41KoqnROkfTm2pZVbKxvbZRuNvKXLRXxs3VfyO0WhY50TQS40EuKO9SW3rBj/sF3WbVwDACeMZyw==",
      "dependencies": {
        "@next/env": "16.1.6",
        "@swc/helpers": "0.5.15",
        "baseline-browser-mapping": "^2.8.3",
        "caniuse-lite": "^1.0.30001579",
        "postcss": "8.4.31",
        "styled-jsx": "5.1.6"
      },
      "bin": {
        "next": "dist/bin/next"
      },
      "engines": {
        "node": ">=20.9.0"
      },
      "optionalDependencies": {
        "@next/swc-darwin-arm64": "16.1.6",
        "@next/swc-darwin-x64": "16.1.6",
        "@next/swc-linux-arm64-gnu": "16.1.6",
        "@next/swc-linux-arm64-musl": "16.1.6",
        "@next/swc-linux-x64-gnu": "16.1.6",
        "@next/swc-linux-x64-musl": "16.1.6",
        "@next/swc-win32-arm64-msvc": "16.1.6",
        "@next/swc-win32-x64-msvc": "16.1.6",
        "sharp": "^0.34.4"
      },
      "peerDependencies": {
        "@opentelemetry/api": "^1.1.0",
        "@playwright/test": "^1.51.1",
        "babel-plugin-react-compiler": "*",
        "react": "^18.2.0 || 19.0.0-rc-de68d2f4-20241204 || ^19.0.0",
        "react-dom": "^18.2.0 || 19.0.0-rc-de68d2f4-20241204 || ^19.0.0",
        "sass": "^1.3.0"
      },
      "peerDependenciesMeta": {
        "@opentelemetry/api": {
          "optional": true
        },
        "@playwright/test": {
          "optional": true
        },
        "babel-plugin-react-compiler": {
          "optional": true
        },
        "sass": {
          "optional": true
        }
      }
    },
    "node_modules/next/node_modules/postcss": {
      "version": "8.4.31",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.4.31.tgz",
      "integrity": "sha512-PS08Iboia9mts/2ygV3eLpY5ghnUcfLV/EXTOW1E2qYxJKGGBUtNjN76FYHnMs36RmARn41bC0AZmn+rR0OVpQ==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "dependencies": {
        "nanoid": "^3.3.6",
        "picocolors": "^1.0.0",
        "source-map-js": "^1.0.2"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/node-releases": {
      "version": "2.0.27",
      "resolved": "https://registry.npmjs.org/node-releases/-/node-releases-2.0.27.tgz",
      "integrity": "sha512-nmh3lCkYZ3grZvqcCH+fjmQ7X+H0OeZgP40OierEaAptX4XofMh5kwNbWh7lBduUzCcV/8kZ+NDLCwm2iorIlA==",
      "dev": true
    },
    "node_modules/normalize-path": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/normalize-path/-/normalize-path-3.0.0.tgz",
      "integrity": "sha512-6eZs5Ls3WtCisHWp9S2GUy8dqkpGi4BVSz3GaqiE6ezub0512ESztXUwUB6C6IKbQkY2Pnb/mD4WYojCRwcwLA==",
      "dev": true,
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/object-assign": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz",
      "integrity": "sha512-rJgTQnkUnH1sFw8yT6VSU3zD3sWmu6sZhIseY8VX+GRu3P6F7Fu+JNDoXfklElbLJSnc3FUQHVe4cU5hj+BcUg==",
      "dev": true,
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/object-hash": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/object-hash/-/object-hash-3.0.0.tgz",
      "integrity": "sha512-RSn9F68PjH9HqtltsSnqYC1XXoWe9Bju5+213R98cNGttag9q9yAOTzdbsqvIa7aNm5WffBZFpWYr2aWrklWAw==",
      "dev": true,
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/object-inspect": {
      "version": "1.13.4",
      "resolved": "https://registry.npmjs.org/object-inspect/-/object-inspect-1.13.4.tgz",
      "integrity": "sha512-W67iLl4J2EXEGTbfeHCffrjDfitvLANg0UlX3wFUUSTx92KXRFegMHUVgSqE+wvhAbi4WqjGg9czysTV2Epbew==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object-keys": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/object-keys/-/object-keys-1.1.1.tgz",
      "integrity": "sha512-NuAESUOUMrlIXOfHKzD6bpPu3tYt3xvjNdRIQ+FeT0lNb4K8WR70CaDxhuNguS2XG+GjkyMwOzsN5ZktImfhLA==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/object.assign": {
      "version": "4.1.7",
      "resolved": "https://registry.npmjs.org/object.assign/-/object.assign-4.1.7.tgz",
      "integrity": "sha512-nK28WOo+QIjBkDduTINE4JkF/UJJKyf2EJxvJKfblDpyg0Q+pkOHNTL0Qwy6NP6FhE/EnzV73BxxqcJaXY9anw==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0",
        "has-symbols": "^1.1.0",
        "object-keys": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object.entries": {
      "version": "1.1.9",
      "resolved": "https://registry.npmjs.org/object.entries/-/object.entries-1.1.9.tgz",
      "integrity": "sha512-8u/hfXFRBD1O0hPUjioLhoWFHRmt6tKA4/vZPyckBr18l1KE9uHrFaFaUi8MDRTpi4uak2goyPTSNJLXX2k2Hw==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/object.fromentries": {
      "version": "2.0.8",
      "resolved": "https://registry.npmjs.org/object.fromentries/-/object.fromentries-2.0.8.tgz",
      "integrity": "sha512-k6E21FzySsSK5a21KRADBd/NGneRegFO5pLHfdQLpRDETUNJueLXs3WCzyQ3tFRDYgbq3KHGXfTbi2bs8WQ6rQ==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.2",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object.groupby": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/object.groupby/-/object.groupby-1.0.3.tgz",
      "integrity": "sha512-+Lhy3TQTuzXI5hevh8sBGqbmurHbbIjAi0Z4S63nthVLmLxfbj4T54a4CfZrXIrt9iP4mVAPYMo/v99taj3wjQ==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/object.values": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/object.values/-/object.values-1.2.1.tgz",
      "integrity": "sha512-gXah6aZrcUxjWg2zR2MwouP2eHlCBzdV4pygudehaKXSGW4v2AsRQUK+lwwXhii6KFZcunEnmSUoYp5CXibxtA==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/optionator": {
      "version": "0.9.4",
      "resolved": "https://registry.npmjs.org/optionator/-/optionator-0.9.4.tgz",
      "integrity": "sha512-6IpQ7mKUxRcZNLIObR0hz7lxsapSSIYNZJwXPGeF0mTVqGKFIXj1DQcMoT22S3ROcLyY/rz0PWaWZ9ayWmad9g==",
      "dev": true,
      "dependencies": {
        "deep-is": "^0.1.3",
        "fast-levenshtein": "^2.0.6",
        "levn": "^0.4.1",
        "prelude-ls": "^1.2.1",
        "type-check": "^0.4.0",
        "word-wrap": "^1.2.5"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/own-keys": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/own-keys/-/own-keys-1.0.1.tgz",
      "integrity": "sha512-qFOyK5PjiWZd+QQIh+1jhdb9LpxTF0qs7Pm8o5QHYZ0M3vKqSqzsZaEB6oWlxZ+q2sJBMI/Ktgd2N5ZwQoRHfg==",
      "dev": true,
      "dependencies": {
        "get-intrinsic": "^1.2.6",
        "object-keys": "^1.1.1",
        "safe-push-apply": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/p-limit": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/p-limit/-/p-limit-3.1.0.tgz",
      "integrity": "sha512-TYOanM3wGwNGsZN2cVTYPArw454xnXj5qmWF1bEoAc4+cU/ol7GVh7odevjp1FNHduHc3KZMcFduxU5Xc6uJRQ==",
      "dev": true,
      "dependencies": {
        "yocto-queue": "^0.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/p-locate": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-5.0.0.tgz",
      "integrity": "sha512-LaNjtRWUBY++zB5nE/NwcaoMylSPk+S+ZHNB1TzdbMJMny6dynpAGt7X/tl/QYq3TIeE6nxHppbo2LGymrG5Pw==",
      "dev": true,
      "dependencies": {
        "p-limit": "^3.0.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/parent-module": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/parent-module/-/parent-module-1.0.1.tgz",
      "integrity": "sha512-GQ2EWRpQV8/o+Aw8YqtfZZPfNRWZYkbidE9k5rpl/hC3vtHHBfGm2Ifi6qWV+coDGkrUKZAxE3Lot5kcsRlh+g==",
      "dev": true,
      "dependencies": {
        "callsites": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/path-exists": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/path-exists/-/path-exists-4.0.0.tgz",
      "integrity": "sha512-ak9Qy5Q7jYb2Wwcey5Fpvg2KoAc/ZIhLSLOSBmRmygPsGwkVVt0fZa0qrtMz+m6tJTAHfZQ8FnmB4MG4LWy7/w==",
      "dev": true,
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-key": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/path-key/-/path-key-3.1.1.tgz",
      "integrity": "sha512-ojmeN0qd+y0jszEtoY48r0Peq5dwMEkIlCOu6Q5f41lfkswXuKtYrhgoTpLnyIcHm24Uhqx+5Tqm2InSwLhE6Q==",
      "dev": true,
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-parse": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/path-parse/-/path-parse-1.0.7.tgz",
      "integrity": "sha512-LDJzPVEEEPR+y48z93A0Ed0yXb8pAByGWo/k5YYdYgpY2/2EsOsksJrq7lOHxryrVOn1ejG6oAp8ahvOIQD8sw==",
      "dev": true
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA=="
    },
    "node_modules/picomatch": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-2.3.1.tgz",
      "integrity": "sha512-JU3teHTNjmE2VCGFzuY8EXzCDVwEqB2a8fsIvwaStHhAWJEeVd1o1QD80CU6+ZdEXXSLbSsuLwJjkCBWqRQUVA==",
      "dev": true,
      "engines": {
        "node": ">=8.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/pify": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/pify/-/pify-2.3.0.tgz",
      "integrity": "sha512-udgsAY+fTnvv7kI7aaxbqwWNb0AHiB0qBO89PZKPkoTmGOgdbrHDKD+0B2X4uTfJ/FT1R09r9gTsjUjNJotuog==",
      "dev": true,
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/pirates": {
      "version": "4.0.7",
      "resolved": "https://registry.npmjs.org/pirates/-/pirates-4.0.7.tgz",
      "integrity": "sha512-TfySrs/5nm8fQJDcBDuUng3VOUKsd7S+zqvbOTiGXHfxX4wK31ard+hoNuvkicM/2YFzlpDgABOevKSsB4G/FA==",
      "dev": true,
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/possible-typed-array-names": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/possible-typed-array-names/-/possible-typed-array-names-1.1.0.tgz",
      "integrity": "sha512-/+5VFTchJDoVj3bhoqi6UeymcD00DAwb1nJwamzPvHEszJ4FpF6SNNbUbOS8yI56qHzdV8eK0qEfOSiodkTdxg==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/postcss": {
      "version": "8.5.6",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.5.6.tgz",
      "integrity": "sha512-3Ybi1tAuwAP9s0r1UQ2J4n5Y0G05bJkpUIO0/bI9MhwmD70S5aTWbXGBwxHrelT+XM1k6dM0pk+SwNkpTRN7Pg==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "dependencies": {
        "nanoid": "^3.3.11",
        "picocolors": "^1.1.1",
        "source-map-js": "^1.2.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/postcss-import": {
      "version": "15.1.0",
      "resolved": "https://registry.npmjs.org/postcss-import/-/postcss-import-15.1.0.tgz",
      "integrity": "sha512-hpr+J05B2FVYUAXHeK1YyI267J/dDDhMU6B6civm8hSY1jYJnBXxzKDKDswzJmtLHryrjhnDjqqp/49t8FALew==",
      "dev": true,
      "dependencies": {
        "postcss-value-parser": "^4.0.0",
        "read-cache": "^1.0.0",
        "resolve": "^1.1.7"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "postcss": "^8.0.0"
      }
    },
    "node_modules/postcss-js": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/postcss-js/-/postcss-js-4.1.0.tgz",
      "integrity": "sha512-oIAOTqgIo7q2EOwbhb8UalYePMvYoIeRY2YKntdpFQXNosSu3vLrniGgmH9OKs/qAkfoj5oB3le/7mINW1LCfw==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "dependencies": {
        "camelcase-css": "^2.0.1"
      },
      "engines": {
        "node": "^12 || ^14 || >= 16"
      },
      "peerDependencies": {
        "postcss": "^8.4.21"
      }
    },
    "node_modules/postcss-load-config": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/postcss-load-config/-/postcss-load-config-6.0.1.tgz",
      "integrity": "sha512-oPtTM4oerL+UXmx+93ytZVN82RrlY/wPUV8IeDxFrzIjXOLF1pN+EmKPLbubvKHT2HC20xXsCAH2Z+CKV6Oz/g==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "dependencies": {
        "lilconfig": "^3.1.1"
      },
      "engines": {
        "node": ">= 18"
      },
      "peerDependencies": {
        "jiti": ">=1.21.0",
        "postcss": ">=8.0.9",
        "tsx": "^4.8.1",
        "yaml": "^2.4.2"
      },
      "peerDependenciesMeta": {
        "jiti": {
          "optional": true
        },
        "postcss": {
          "optional": true
        },
        "tsx": {
          "optional": true
        },
        "yaml": {
          "optional": true
        }
      }
    },
    "node_modules/postcss-nested": {
      "version": "6.2.0",
      "resolved": "https://registry.npmjs.org/postcss-nested/-/postcss-nested-6.2.0.tgz",
      "integrity": "sha512-HQbt28KulC5AJzG+cZtj9kvKB93CFCdLvog1WFLf1D+xmMvPGlBstkpTEZfK5+AN9hfJocyBFCNiqyS48bpgzQ==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "dependencies": {
        "postcss-selector-parser": "^6.1.1"
      },
      "engines": {
        "node": ">=12.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.14"
      }
    },
    "node_modules/postcss-selector-parser": {
      "version": "6.1.2",
      "resolved": "https://registry.npmjs.org/postcss-selector-parser/-/postcss-selector-parser-6.1.2.tgz",
      "integrity": "sha512-Q8qQfPiZ+THO/3ZrOrO0cJJKfpYCagtMUkXbnEfmgUjwXg6z/WBeOyS9APBBPCTSiDV+s4SwQGu8yFsiMRIudg==",
      "dev": true,
      "dependencies": {
        "cssesc": "^3.0.0",
        "util-deprecate": "^1.0.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/postcss-value-parser": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/postcss-value-parser/-/postcss-value-parser-4.2.0.tgz",
      "integrity": "sha512-1NNCs6uurfkVbeXG4S8JFT9t19m45ICnif8zWLd5oPSZ50QnwMfK+H3jv408d4jw/7Bttv5axS5IiHoLaVNHeQ==",
      "dev": true
    },
    "node_modules/prelude-ls": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/prelude-ls/-/prelude-ls-1.2.1.tgz",
      "integrity": "sha512-vkcDPrRZo1QZLbn5RLGPpg/WmIQ65qoWWhcGKf/b5eplkkarX0m9z8ppCat4mlOqUsWpyNuYgO3VRyrYHSzX5g==",
      "dev": true,
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/prop-types": {
      "version": "15.8.1",
      "resolved": "https://registry.npmjs.org/prop-types/-/prop-types-15.8.1.tgz",
      "integrity": "sha512-oj87CgZICdulUohogVAR7AjlC0327U4el4L6eAvOqCeudMDVU0NThNaV+b9Df4dXgSP1gXMTnPdhfe/2qDH5cg==",
      "dev": true,
      "dependencies": {
        "loose-envify": "^1.4.0",
        "object-assign": "^4.1.1",
        "react-is": "^16.13.1"
      }
    },
    "node_modules/punycode": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/punycode/-/punycode-2.3.1.tgz",
      "integrity": "sha512-vYt7UD1U9Wg6138shLtLOvdAu+8DsC/ilFtEVHcH+wydcSpNE20AfSOduf6MkRFahL5FY7X1oU7nKVZFtfq8Fg==",
      "dev": true,
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/queue-microtask": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/queue-microtask/-/queue-microtask-1.2.3.tgz",
      "integrity": "sha512-NuaNSa6flKT5JaSYQzJok04JzTL1CA6aGhv5rfLW3PgqA+M2ChpZQnAC8h8i4ZFkBS8X5RqkDBHA7r4hej3K9A==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ]
    },
    "node_modules/react": {
      "version": "19.2.3",
      "resolved": "https://registry.npmjs.org/react/-/react-19.2.3.tgz",
      "integrity": "sha512-Ku/hhYbVjOQnXDZFv2+RibmLFGwFdeeKHFcOTlrt7xplBnya5OGn/hIRDsqDiSUcfORsDC7MPxwork8jBwsIWA==",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-dom": {
      "version": "19.2.3",
      "resolved": "https://registry.npmjs.org/react-dom/-/react-dom-19.2.3.tgz",
      "integrity": "sha512-yELu4WmLPw5Mr/lmeEpox5rw3RETacE++JgHqQzd2dg+YbJuat3jH4ingc+WPZhxaoFzdv9y33G+F7Nl5O0GBg==",
      "dependencies": {
        "scheduler": "^0.27.0"
      },
      "peerDependencies": {
        "react": "^19.2.3"
      }
    },
    "node_modules/react-is": {
      "version": "16.13.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-16.13.1.tgz",
      "integrity": "sha512-24e6ynE2H+OKt4kqsOvNd8kBpV65zoxbA4BVsEOB3ARVWQki/DHzaUoC5KuON/BiccDaCCTZBuOcfZs70kR8bQ==",
      "dev": true
    },
    "node_modules/read-cache": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/read-cache/-/read-cache-1.0.0.tgz",
      "integrity": "sha512-Owdv/Ft7IjOgm/i0xvNDZ1LrRANRfew4b2prF3OWMQLxLfu3bS8FVhCsrSCMK4lR56Y9ya+AThoTpDCTxCmpRA==",
      "dev": true,
      "dependencies": {
        "pify": "^2.3.0"
      }
    },
    "node_modules/readdirp": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/readdirp/-/readdirp-3.6.0.tgz",
      "integrity": "sha512-hOS089on8RduqdbhvQ5Z37A0ESjsqz6qnRcffsMU3495FuTdqSm+7bhJ29JvIOsBDEEnan5DPu9t3To9VRlMzA==",
      "dev": true,
      "dependencies": {
        "picomatch": "^2.2.1"
      },
      "engines": {
        "node": ">=8.10.0"
      }
    },
    "node_modules/reflect.getprototypeof": {
      "version": "1.0.10",
      "resolved": "https://registry.npmjs.org/reflect.getprototypeof/-/reflect.getprototypeof-1.0.10.tgz",
      "integrity": "sha512-00o4I+DVrefhv+nX0ulyi3biSHCPDe+yLv5o/p6d/UVlirijB8E16FtfwSAi4g3tcqrQ4lRAqQSoFEZJehYEcw==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.9",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.7",
        "get-proto": "^1.0.1",
        "which-builtin-type": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/regexp.prototype.flags": {
      "version": "1.5.4",
      "resolved": "https://registry.npmjs.org/regexp.prototype.flags/-/regexp.prototype.flags-1.5.4.tgz",
      "integrity": "sha512-dYqgNSZbDwkaJ2ceRd9ojCGjBq+mOm9LmtXnAnEGyHhN/5R7iDW2TRw3h+o/jCFxus3P2LfWIIiwowAjANm7IA==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-errors": "^1.3.0",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "set-function-name": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/resolve": {
      "version": "1.22.11",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-1.22.11.tgz",
      "integrity": "sha512-RfqAvLnMl313r7c9oclB1HhUEAezcpLjz95wFH4LVuhk9JF/r22qmVP9AMmOU4vMX7Q8pN8jwNg/CSpdFnMjTQ==",
      "dev": true,
      "dependencies": {
        "is-core-module": "^2.16.1",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/resolve-from": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/resolve-from/-/resolve-from-4.0.0.tgz",
      "integrity": "sha512-pb/MYmXstAkysRFx8piNI1tGFNQIFA3vkE3Gq4EuA1dF6gHp/+vgZqsCGJapvy8N3Q+4o7FwvquPJcnZ7RYy4g==",
      "dev": true,
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/resolve-pkg-maps": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/resolve-pkg-maps/-/resolve-pkg-maps-1.0.0.tgz",
      "integrity": "sha512-seS2Tj26TBVOC2NIc2rOe2y2ZO7efxITtLZcGSOnHHNOQ7CkiUBfw0Iw2ck6xkIhPwLhKNLS8BO+hEpngQlqzw==",
      "dev": true,
      "funding": {
        "url": "https://github.com/privatenumber/resolve-pkg-maps?sponsor=1"
      }
    },
    "node_modules/reusify": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/reusify/-/reusify-1.1.0.tgz",
      "integrity": "sha512-g6QUff04oZpHs0eG5p83rFLhHeV00ug/Yf9nZM6fLeUrPguBTkTQOdpAWWspMh55TZfVQDPaN3NQJfbVRAxdIw==",
      "dev": true,
      "engines": {
        "iojs": ">=1.0.0",
        "node": ">=0.10.0"
      }
    },
    "node_modules/run-parallel": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/run-parallel/-/run-parallel-1.2.0.tgz",
      "integrity": "sha512-5l4VyZR86LZ/lDxZTR6jqL8AFE2S0IFLMP26AbjsLVADxHdhB/c0GUsH+y39UfCi3dzz8OlQuPmnaJOMoDHQBA==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "dependencies": {
        "queue-microtask": "^1.2.2"
      }
    },
    "node_modules/safe-array-concat": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/safe-array-concat/-/safe-array-concat-1.1.3.tgz",
      "integrity": "sha512-AURm5f0jYEOydBj7VQlVvDrjeFgthDdEF5H1dP+6mNpoXOMo1quQqJ4wvJDyRZ9+pO3kGWoOdmV08cSv2aJV6Q==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "get-intrinsic": "^1.2.6",
        "has-symbols": "^1.1.0",
        "isarray": "^2.0.5"
      },
      "engines": {
        "node": ">=0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/safe-push-apply": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/safe-push-apply/-/safe-push-apply-1.0.0.tgz",
      "integrity": "sha512-iKE9w/Z7xCzUMIZqdBsp6pEQvwuEebH4vdpjcDWnyzaI6yl6O9FHvVpmGelvEHNsoY6wGblkxR6Zty/h00WiSA==",
      "dev": true,
      "dependencies": {
        "es-errors": "^1.3.0",
        "isarray": "^2.0.5"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/safe-regex-test": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/safe-regex-test/-/safe-regex-test-1.1.0.tgz",
      "integrity": "sha512-x/+Cz4YrimQxQccJf5mKEbIa1NzeCRNI5Ecl/ekmlYaampdNLPalVyIcCZNNH3MvmqBugV5TMYZXv0ljslUlaw==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "is-regex": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/scheduler": {
      "version": "0.27.0",
      "resolved": "https://registry.npmjs.org/scheduler/-/scheduler-0.27.0.tgz",
      "integrity": "sha512-eNv+WrVbKu1f3vbYJT/xtiF5syA5HPIMtf9IgY/nKg0sWqzAUEvqY/xm7OcZc/qafLx/iO9FgOmeSAp4v5ti/Q=="
    },
    "node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "dev": true,
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/set-function-length": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/set-function-length/-/set-function-length-1.2.2.tgz",
      "integrity": "sha512-pgRc4hJ4/sNjWCSS9AmnS40x3bNMDTknHgL5UaMBTMyJnU90EgWh1Rz+MC9eFu4BuN/UwZjKQuY/1v3rM7HMfg==",
      "dev": true,
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2",
        "get-intrinsic": "^1.2.4",
        "gopd": "^1.0.1",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/set-function-name": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/set-function-name/-/set-function-name-2.0.2.tgz",
      "integrity": "sha512-7PGFlmtwsEADb0WYyvCMa1t+yke6daIG4Wirafur5kcf+MhUnPms1UeR0CKQdTZD81yESwMHbtn+TR+dMviakQ==",
      "dev": true,
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-errors": "^1.3.0",
        "functions-have-names": "^1.2.3",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/set-proto": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/set-proto/-/set-proto-1.0.0.tgz",
      "integrity": "sha512-RJRdvCo6IAnPdsvP/7m6bsQqNnn1FCBX5ZNtFL98MmFF/4xAIJTIg1YbHW5DC2W5SKZanrC6i4HsJqlajw/dZw==",
      "dev": true,
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/sharp": {
      "version": "0.34.5",
      "resolved": "https://registry.npmjs.org/sharp/-/sharp-0.34.5.tgz",
      "integrity": "sha512-Ou9I5Ft9WNcCbXrU9cMgPBcCK8LiwLqcbywW3t4oDV37n1pzpuNLsYiAV8eODnjbtQlSDwZ2cUEeQz4E54Hltg==",
      "hasInstallScript": true,
      "optional": true,
      "dependencies": {
        "@img/colour": "^1.0.0",
        "detect-libc": "^2.1.2",
        "semver": "^7.7.3"
      },
      "engines": {
        "node": "^18.17.0 || ^20.3.0 || >=21.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/libvips"
      },
      "optionalDependencies": {
        "@img/sharp-darwin-arm64": "0.34.5",
        "@img/sharp-darwin-x64": "0.34.5",
        "@img/sharp-libvips-darwin-arm64": "1.2.4",
        "@img/sharp-libvips-darwin-x64": "1.2.4",
        "@img/sharp-libvips-linux-arm": "1.2.4",
        "@img/sharp-libvips-linux-arm64": "1.2.4",
        "@img/sharp-libvips-linux-ppc64": "1.2.4",
        "@img/sharp-libvips-linux-riscv64": "1.2.4",
        "@img/sharp-libvips-linux-s390x": "1.2.4",
        "@img/sharp-libvips-linux-x64": "1.2.4",
        "@img/sharp-libvips-linuxmusl-arm64": "1.2.4",
        "@img/sharp-libvips-linuxmusl-x64": "1.2.4",
        "@img/sharp-linux-arm": "0.34.5",
        "@img/sharp-linux-arm64": "0.34.5",
        "@img/sharp-linux-ppc64": "0.34.5",
        "@img/sharp-linux-riscv64": "0.34.5",
        "@img/sharp-linux-s390x": "0.34.5",
        "@img/sharp-linux-x64": "0.34.5",
        "@img/sharp-linuxmusl-arm64": "0.34.5",
        "@img/sharp-linuxmusl-x64": "0.34.5",
        "@img/sharp-wasm32": "0.34.5",
        "@img/sharp-win32-arm64": "0.34.5",
        "@img/sharp-win32-ia32": "0.34.5",
        "@img/sharp-win32-x64": "0.34.5"
      }
    },
    "node_modules/sharp/node_modules/semver": {
      "version": "7.7.3",
      "resolved": "https://registry.npmjs.org/semver/-/semver-7.7.3.tgz",
      "integrity": "sha512-SdsKMrI9TdgjdweUSR9MweHA4EJ8YxHn8DFaDisvhVlUOe4BF1tLD7GAj0lIqWVl+dPb/rExr0Btby5loQm20Q==",
      "optional": true,
      "bin": {
        "semver": "bin/semver.js"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/shebang-command": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/shebang-command/-/shebang-command-2.0.0.tgz",
      "integrity": "sha512-kHxr2zZpYtdmrN1qDjrrX/Z1rR1kG8Dx+gkpK1G4eXmvXswmcE1hTWBWYUzlraYw1/yZp6YuDY77YtvbN0dmDA==",
      "dev": true,
      "dependencies": {
        "shebang-regex": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/shebang-regex": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/shebang-regex/-/shebang-regex-3.0.0.tgz",
      "integrity": "sha512-7++dFhtcx3353uBaq8DDR4NuxBetBzC7ZQOhmTQInHEd6bSrXdiEyzCvG07Z44UYdLShWUyXt5M/yhz8ekcb1A==",
      "dev": true,
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/side-channel": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/side-channel/-/side-channel-1.1.0.tgz",
      "integrity": "sha512-ZX99e6tRweoUXqR+VBrslhda51Nh5MTQwou5tnUDgbtyM0dBgmhEDtWGP/xbKn6hqfPRHujUNwz5fy/wbbhnpw==",
      "dev": true,
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.3",
        "side-channel-list": "^1.0.0",
        "side-channel-map": "^1.0.1",
        "side-channel-weakmap": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-list": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/side-channel-list/-/side-channel-list-1.0.0.tgz",
      "integrity": "sha512-FCLHtRD/gnpCiCHEiJLOwdmFP+wzCmDEkc9y7NsYxeF4u7Btsn1ZuwgwJGxImImHicJArLP4R0yX4c2KCrMrTA==",
      "dev": true,
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-map": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/side-channel-map/-/side-channel-map-1.0.1.tgz",
      "integrity": "sha512-VCjCNfgMsby3tTdo02nbjtM/ewra6jPHmpThenkTYh8pG9ucZ/1P8So4u4FGBek/BjpOVsDCMoLA/iuBKIFXRA==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-weakmap": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/side-channel-weakmap/-/side-channel-weakmap-1.0.2.tgz",
      "integrity": "sha512-WPS/HvHQTYnHisLo9McqBHOJk2FkHO/tlpvldyrnem4aeQp4hai3gythswg6p01oSoTl58rcpiFAjF2br2Ak2A==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3",
        "side-channel-map": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/source-map-js": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.1.tgz",
      "integrity": "sha512-UXWMKhLOwVKb728IUtQPXxfYU+usdybtUrK/8uGE8CQMvrhOpwvzDBwj0QhSL7MQc7vIsISBG8VQ8+IDQxpfQA==",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/stable-hash": {
      "version": "0.0.5",
      "resolved": "https://registry.npmjs.org/stable-hash/-/stable-hash-0.0.5.tgz",
      "integrity": "sha512-+L3ccpzibovGXFK+Ap/f8LOS0ahMrHTf3xu7mMLSpEGU0EO9ucaysSylKo9eRDFNhWve/y275iPmIZ4z39a9iA==",
      "dev": true
    },
    "node_modules/stop-iteration-iterator": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/stop-iteration-iterator/-/stop-iteration-iterator-1.1.0.tgz",
      "integrity": "sha512-eLoXW/DHyl62zxY4SCaIgnRhuMr6ri4juEYARS8E6sCEqzKpOiE521Ucofdx+KnDZl5xmvGYaaKCk5FEOxJCoQ==",
      "dev": true,
      "dependencies": {
        "es-errors": "^1.3.0",
        "internal-slot": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/string.prototype.includes": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/string.prototype.includes/-/string.prototype.includes-2.0.1.tgz",
      "integrity": "sha512-o7+c9bW6zpAdJHTtujeePODAhkuicdAryFsfVKwA+wGw89wJ4GTY484WTucM9hLtDEOpOvI+aHnzqnC5lHp4Rg==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.3"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/string.prototype.matchall": {
      "version": "4.0.12",
      "resolved": "https://registry.npmjs.org/string.prototype.matchall/-/string.prototype.matchall-4.0.12.tgz",
      "integrity": "sha512-6CC9uyBL+/48dYizRf7H7VAYCMCNTBeM78x/VTUe9bFEaxBepPJDa1Ow99LqI/1yF7kuy7Q3cQsYMrcjGUcskA==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.6",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.6",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "internal-slot": "^1.1.0",
        "regexp.prototype.flags": "^1.5.3",
        "set-function-name": "^2.0.2",
        "side-channel": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.repeat": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/string.prototype.repeat/-/string.prototype.repeat-1.0.0.tgz",
      "integrity": "sha512-0u/TldDbKD8bFCQ/4f5+mNRrXwZ8hg2w7ZR8wa16e8z9XpePWl3eGEcUD0OXpEH/VJH/2G3gjUtR3ZOiBe2S/w==",
      "dev": true,
      "dependencies": {
        "define-properties": "^1.1.3",
        "es-abstract": "^1.17.5"
      }
    },
    "node_modules/string.prototype.trim": {
      "version": "1.2.10",
      "resolved": "https://registry.npmjs.org/string.prototype.trim/-/string.prototype.trim-1.2.10.tgz",
      "integrity": "sha512-Rs66F0P/1kedk5lyYyH9uBzuiI/kNRmwJAR9quK6VOtIpZ2G+hMZd+HQbbv25MgCA6gEffoMZYxlTod4WcdrKA==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "define-data-property": "^1.1.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-object-atoms": "^1.0.0",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.trimend": {
      "version": "1.0.9",
      "resolved": "https://registry.npmjs.org/string.prototype.trimend/-/string.prototype.trimend-1.0.9.tgz",
      "integrity": "sha512-G7Ok5C6E/j4SGfyLCloXTrngQIQU3PWtXGst3yM7Bea9FRURf1S42ZHlZZtsNque2FN2PoUhfZXYLNWwEr4dLQ==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.trimstart": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/string.prototype.trimstart/-/string.prototype.trimstart-1.0.8.tgz",
      "integrity": "sha512-UXSH262CSZY1tfu3G3Secr6uGLCFVPMhIqHjlgCUtCCcgihYc/xKs9djMTMUOb2j1mVSeU8EU6NWc/iQKU6Gfg==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/strip-bom": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/strip-bom/-/strip-bom-3.0.0.tgz",
      "integrity": "sha512-vavAMRXOgBVNF6nyEEmL3DBK19iRpDcoIwW+swQ+CbGiu7lju6t+JklA1MHweoWtadgt4ISVUsXLyDq34ddcwA==",
      "dev": true,
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/strip-json-comments": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/strip-json-comments/-/strip-json-comments-3.1.1.tgz",
      "integrity": "sha512-6fPc+R4ihwqP6N/aIv2f1gMH8lOVtWQHoqC4yK6oSDVVocumAsfCqjkXnqiYMhmMwS/mEHLp7Vehlt3ql6lEig==",
      "dev": true,
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/styled-jsx": {
      "version": "5.1.6",
      "resolved": "https://registry.npmjs.org/styled-jsx/-/styled-jsx-5.1.6.tgz",
      "integrity": "sha512-qSVyDTeMotdvQYoHWLNGwRFJHC+i+ZvdBRYosOFgC+Wg1vx4frN2/RG/NA7SYqqvKNLf39P2LSRA2pu6n0XYZA==",
      "dependencies": {
        "client-only": "0.0.1"
      },
      "engines": {
        "node": ">= 12.0.0"
      },
      "peerDependencies": {
        "react": ">= 16.8.0 || 17.x.x || ^18.0.0-0 || ^19.0.0-0"
      },
      "peerDependenciesMeta": {
        "@babel/core": {
          "optional": true
        },
        "babel-plugin-macros": {
          "optional": true
        }
      }
    },
    "node_modules/sucrase": {
      "version": "3.35.1",
      "resolved": "https://registry.npmjs.org/sucrase/-/sucrase-3.35.1.tgz",
      "integrity": "sha512-DhuTmvZWux4H1UOnWMB3sk0sbaCVOoQZjv8u1rDoTV0HTdGem9hkAZtl4JZy8P2z4Bg0nT+YMeOFyVr4zcG5Tw==",
      "dev": true,
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.2",
        "commander": "^4.0.0",
        "lines-and-columns": "^1.1.6",
        "mz": "^2.7.0",
        "pirates": "^4.0.1",
        "tinyglobby": "^0.2.11",
        "ts-interface-checker": "^0.1.9"
      },
      "bin": {
        "sucrase": "bin/sucrase",
        "sucrase-node": "bin/sucrase-node"
      },
      "engines": {
        "node": ">=16 || 14 >=14.17"
      }
    },
    "node_modules/supports-color": {
      "version": "7.2.0",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-7.2.0.tgz",
      "integrity": "sha512-qpCAvRl9stuOHveKsn7HncJRvv501qIacKzQlO/+Lwxc9+0q2wLyv4Dfvt80/DPn2pqOBsJdDiogXGR9+OvwRw==",
      "dev": true,
      "dependencies": {
        "has-flag": "^4.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/supports-preserve-symlinks-flag": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/supports-preserve-symlinks-flag/-/supports-preserve-symlinks-flag-1.0.0.tgz",
      "integrity": "sha512-ot0WnXS9fgdkgIcePe6RHNk1WA8+muPa6cSjeR3V8K27q9BB1rTE3R1p7Hv0z1ZyAc8s6Vvv8DIyWf681MAt0w==",
      "dev": true,
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/tailwindcss": {
      "version": "3.4.19",
      "resolved": "https://registry.npmjs.org/tailwindcss/-/tailwindcss-3.4.19.tgz",
      "integrity": "sha512-3ofp+LL8E+pK/JuPLPggVAIaEuhvIz4qNcf3nA1Xn2o/7fb7s/TYpHhwGDv1ZU3PkBluUVaF8PyCHcm48cKLWQ==",
      "dev": true,
      "dependencies": {
        "@alloc/quick-lru": "^5.2.0",
        "arg": "^5.0.2",
        "chokidar": "^3.6.0",
        "didyoumean": "^1.2.2",
        "dlv": "^1.1.3",
        "fast-glob": "^3.3.2",
        "glob-parent": "^6.0.2",
        "is-glob": "^4.0.3",
        "jiti": "^1.21.7",
        "lilconfig": "^3.1.3",
        "micromatch": "^4.0.8",
        "normalize-path": "^3.0.0",
        "object-hash": "^3.0.0",
        "picocolors": "^1.1.1",
        "postcss": "^8.4.47",
        "postcss-import": "^15.1.0",
        "postcss-js": "^4.0.1",
        "postcss-load-config": "^4.0.2 || ^5.0 || ^6.0",
        "postcss-nested": "^6.2.0",
        "postcss-selector-parser": "^6.1.2",
        "resolve": "^1.22.8",
        "sucrase": "^3.35.0"
      },
      "bin": {
        "tailwind": "lib/cli.js",
        "tailwindcss": "lib/cli.js"
      },
      "engines": {
        "node": ">=14.0.0"
      }
    },
    "node_modules/tailwindcss/node_modules/fast-glob": {
      "version": "3.3.3",
      "resolved": "https://registry.npmjs.org/fast-glob/-/fast-glob-3.3.3.tgz",
      "integrity": "sha512-7MptL8U0cqcFdzIzwOTHoilX9x5BrNqye7Z/LuC7kCMRio1EMSyqRK3BEAUD7sXRq4iT4AzTVuZdhgQ2TCvYLg==",
      "dev": true,
      "dependencies": {
        "@nodelib/fs.stat": "^2.0.2",
        "@nodelib/fs.walk": "^1.2.3",
        "glob-parent": "^5.1.2",
        "merge2": "^1.3.0",
        "micromatch": "^4.0.8"
      },
      "engines": {
        "node": ">=8.6.0"
      }
    },
    "node_modules/tailwindcss/node_modules/fast-glob/node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "dev": true,
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/thenify": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/thenify/-/thenify-3.3.1.tgz",
      "integrity": "sha512-RVZSIV5IG10Hk3enotrhvz0T9em6cyHBLkH/YAZuKqd8hRkKhSfCGIcP2KUY0EPxndzANBmNllzWPwak+bheSw==",
      "dev": true,
      "dependencies": {
        "any-promise": "^1.0.0"
      }
    },
    "node_modules/thenify-all": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/thenify-all/-/thenify-all-1.6.0.tgz",
      "integrity": "sha512-RNxQH/qI8/t3thXJDwcstUO4zeqo64+Uy/+sNVRBx4Xn2OX+OZ9oP+iJnNFqplFra2ZUVeKCSa2oVWi3T4uVmA==",
      "dev": true,
      "dependencies": {
        "thenify": ">= 3.1.0 < 4"
      },
      "engines": {
        "node": ">=0.8"
      }
    },
    "node_modules/tinyglobby": {
      "version": "0.2.15",
      "resolved": "https://registry.npmjs.org/tinyglobby/-/tinyglobby-0.2.15.tgz",
      "integrity": "sha512-j2Zq4NyQYG5XMST4cbs02Ak8iJUdxRM0XI5QyxXuZOzKOINmWurp3smXu3y5wDcJrptwpSjgXHzIQxR0omXljQ==",
      "dev": true,
      "dependencies": {
        "fdir": "^6.5.0",
        "picomatch": "^4.0.3"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/SuperchupuDev"
      }
    },
    "node_modules/tinyglobby/node_modules/fdir": {
      "version": "6.5.0",
      "resolved": "https://registry.npmjs.org/fdir/-/fdir-6.5.0.tgz",
      "integrity": "sha512-tIbYtZbucOs0BRGqPJkshJUYdL+SDH7dVM8gjy+ERp3WAUjLEFJE+02kanyHtwjWOnwrKYBiwAmM0p4kLJAnXg==",
      "dev": true,
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "picomatch": "^3 || ^4"
      },
      "peerDependenciesMeta": {
        "picomatch": {
          "optional": true
        }
      }
    },
    "node_modules/tinyglobby/node_modules/picomatch": {
      "version": "4.0.3",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-4.0.3.tgz",
      "integrity": "sha512-5gTmgEY/sqK6gFXLIsQNH19lWb4ebPDLA4SdLP7dsWkIXHWlG66oPuVvXSGFPppYZz8ZDZq0dYYrbHfBCVUb1Q==",
      "dev": true,
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/to-regex-range": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/to-regex-range/-/to-regex-range-5.0.1.tgz",
      "integrity": "sha512-65P7iz6X5yEr1cwcgvQxbbIw7Uk3gOy5dIdtZ4rDveLqhrdJP+Li/Hx6tyK0NEb+2GCyneCMJiGqrADCSNk8sQ==",
      "dev": true,
      "dependencies": {
        "is-number": "^7.0.0"
      },
      "engines": {
        "node": ">=8.0"
      }
    },
    "node_modules/ts-api-utils": {
      "version": "2.4.0",
      "resolved": "https://registry.npmjs.org/ts-api-utils/-/ts-api-utils-2.4.0.tgz",
      "integrity": "sha512-3TaVTaAv2gTiMB35i3FiGJaRfwb3Pyn/j3m/bfAvGe8FB7CF6u+LMYqYlDh7reQf7UNvoTvdfAqHGmPGOSsPmA==",
      "dev": true,
      "engines": {
        "node": ">=18.12"
      },
      "peerDependencies": {
        "typescript": ">=4.8.4"
      }
    },
    "node_modules/ts-interface-checker": {
      "version": "0.1.13",
      "resolved": "https://registry.npmjs.org/ts-interface-checker/-/ts-interface-checker-0.1.13.tgz",
      "integrity": "sha512-Y/arvbn+rrz3JCKl9C4kVNfTfSm2/mEp5FSz5EsZSANGPSlQrpRI5M4PKF+mJnE52jOO90PnPSc3Ur3bTQw0gA==",
      "dev": true
    },
    "node_modules/tsconfig-paths": {
      "version": "3.15.0",
      "resolved": "https://registry.npmjs.org/tsconfig-paths/-/tsconfig-paths-3.15.0.tgz",
      "integrity": "sha512-2Ac2RgzDe/cn48GvOe3M+o82pEFewD3UPbyoUHHdKasHwJKjds4fLXWf/Ux5kATBKN20oaFGu+jbElp1pos0mg==",
      "dev": true,
      "dependencies": {
        "@types/json5": "^0.0.29",
        "json5": "^1.0.2",
        "minimist": "^1.2.6",
        "strip-bom": "^3.0.0"
      }
    },
    "node_modules/tsconfig-paths/node_modules/json5": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/json5/-/json5-1.0.2.tgz",
      "integrity": "sha512-g1MWMLBiz8FKi1e4w0UyVL3w+iJceWAFBAaBnnGKOpNa5f8TLktkbre1+s6oICydWAm+HRUGTmI+//xv2hvXYA==",
      "dev": true,
      "dependencies": {
        "minimist": "^1.2.0"
      },
      "bin": {
        "json5": "lib/cli.js"
      }
    },
    "node_modules/tslib": {
      "version": "2.8.1",
      "resolved": "https://registry.npmjs.org/tslib/-/tslib-2.8.1.tgz",
      "integrity": "sha512-oJFu94HQb+KVduSUQL7wnpmqnfmLsOA/nAh6b6EH0wCEoK0/mPeXU6c3wKDV83MkOuHPRHtSXKKU99IBazS/2w=="
    },
    "node_modules/type-check": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/type-check/-/type-check-0.4.0.tgz",
      "integrity": "sha512-XleUoc9uwGXqjWwXaUTZAmzMcFZ5858QA2vvx1Ur5xIcixXIP+8LnFDgRplU30us6teqdlskFfu+ae4K79Ooew==",
      "dev": true,
      "dependencies": {
        "prelude-ls": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/typed-array-buffer": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/typed-array-buffer/-/typed-array-buffer-1.0.3.tgz",
      "integrity": "sha512-nAYYwfY3qnzX30IkA6AQZjVbtK6duGontcQm1WSG1MD94YLqK0515GNApXkoxKOWMusVssAHWLh9SeaoefYFGw==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-typed-array": "^1.1.14"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/typed-array-byte-length": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/typed-array-byte-length/-/typed-array-byte-length-1.0.3.tgz",
      "integrity": "sha512-BaXgOuIxz8n8pIq3e7Atg/7s+DpiYrxn4vdot3w9KbnBhcRQq6o3xemQdIfynqSeXeDrF32x+WvfzmOjPiY9lg==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.8",
        "for-each": "^0.3.3",
        "gopd": "^1.2.0",
        "has-proto": "^1.2.0",
        "is-typed-array": "^1.1.14"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typed-array-byte-offset": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/typed-array-byte-offset/-/typed-array-byte-offset-1.0.4.tgz",
      "integrity": "sha512-bTlAFB/FBYMcuX81gbL4OcpH5PmlFHqlCCpAl8AlEzMz5k53oNDvN8p1PNOWLEmI2x4orp3raOFB51tv9X+MFQ==",
      "dev": true,
      "dependencies": {
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "for-each": "^0.3.3",
        "gopd": "^1.2.0",
        "has-proto": "^1.2.0",
        "is-typed-array": "^1.1.15",
        "reflect.getprototypeof": "^1.0.9"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typed-array-length": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/typed-array-length/-/typed-array-length-1.0.7.tgz",
      "integrity": "sha512-3KS2b+kL7fsuk/eJZ7EQdnEmQoaho/r6KUef7hxvltNA5DR8NAUM+8wJMbJyZ4G9/7i3v5zPBIMN5aybAh2/Jg==",
      "dev": true,
      "dependencies": {
        "call-bind": "^1.0.7",
        "for-each": "^0.3.3",
        "gopd": "^1.0.1",
        "is-typed-array": "^1.1.13",
        "possible-typed-array-names": "^1.0.0",
        "reflect.getprototypeof": "^1.0.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typescript": {
      "version": "5.9.3",
      "resolved": "https://registry.npmjs.org/typescript/-/typescript-5.9.3.tgz",
      "integrity": "sha512-jl1vZzPDinLr9eUt3J/t7V6FgNEw9QjvBPdysz9KfQDD41fQrC2Y4vKQdiaUpFT4bXlb1RHhLpp8wtm6M5TgSw==",
      "dev": true,
      "bin": {
        "tsc": "bin/tsc",
        "tsserver": "bin/tsserver"
      },
      "engines": {
        "node": ">=14.17"
      }
    },
    "node_modules/typescript-eslint": {
      "version": "8.54.0",
      "resolved": "https://registry.npmjs.org/typescript-eslint/-/typescript-eslint-8.54.0.tgz",
      "integrity": "sha512-CKsJ+g53QpsNPqbzUsfKVgd3Lny4yKZ1pP4qN3jdMOg/sisIDLGyDMezycquXLE5JsEU0wp3dGNdzig0/fmSVQ==",
      "dev": true,
      "dependencies": {
        "@typescript-eslint/eslint-plugin": "8.54.0",
        "@typescript-eslint/parser": "8.54.0",
        "@typescript-eslint/typescript-estree": "8.54.0",
        "@typescript-eslint/utils": "8.54.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^8.57.0 || ^9.0.0",
        "typescript": ">=4.8.4 <6.0.0"
      }
    },
    "node_modules/unbox-primitive": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/unbox-primitive/-/unbox-primitive-1.1.0.tgz",
      "integrity": "sha512-nWJ91DjeOkej/TA8pXQ3myruKpKEYgqvpw9lz4OPHj/NWFNluYrjbz9j01CJ8yKQd2g4jFoOkINCTW2I5LEEyw==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-bigints": "^1.0.2",
        "has-symbols": "^1.1.0",
        "which-boxed-primitive": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/undici-types": {
      "version": "6.21.0",
      "resolved": "https://registry.npmjs.org/undici-types/-/undici-types-6.21.0.tgz",
      "integrity": "sha512-iwDZqg0QAGrg9Rav5H4n0M64c3mkR59cJ6wQp+7C4nI0gsmExaedaYLNO44eT4AtBBwjbTiGPMlt2Md0T9H9JQ==",
      "dev": true
    },
    "node_modules/unrs-resolver": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/unrs-resolver/-/unrs-resolver-1.11.1.tgz",
      "integrity": "sha512-bSjt9pjaEBnNiGgc9rUiHGKv5l4/TGzDmYw3RhnkJGtLhbnnA/5qJj7x3dNDCRx/PJxu774LlH8lCOlB4hEfKg==",
      "dev": true,
      "hasInstallScript": true,
      "dependencies": {
        "napi-postinstall": "^0.3.0"
      },
      "funding": {
        "url": "https://opencollective.com/unrs-resolver"
      },
      "optionalDependencies": {
        "@unrs/resolver-binding-android-arm-eabi": "1.11.1",
        "@unrs/resolver-binding-android-arm64": "1.11.1",
        "@unrs/resolver-binding-darwin-arm64": "1.11.1",
        "@unrs/resolver-binding-darwin-x64": "1.11.1",
        "@unrs/resolver-binding-freebsd-x64": "1.11.1",
        "@unrs/resolver-binding-linux-arm-gnueabihf": "1.11.1",
        "@unrs/resolver-binding-linux-arm-musleabihf": "1.11.1",
        "@unrs/resolver-binding-linux-arm64-gnu": "1.11.1",
        "@unrs/resolver-binding-linux-arm64-musl": "1.11.1",
        "@unrs/resolver-binding-linux-ppc64-gnu": "1.11.1",
        "@unrs/resolver-binding-linux-riscv64-gnu": "1.11.1",
        "@unrs/resolver-binding-linux-riscv64-musl": "1.11.1",
        "@unrs/resolver-binding-linux-s390x-gnu": "1.11.1",
        "@unrs/resolver-binding-linux-x64-gnu": "1.11.1",
        "@unrs/resolver-binding-linux-x64-musl": "1.11.1",
        "@unrs/resolver-binding-wasm32-wasi": "1.11.1",
        "@unrs/resolver-binding-win32-arm64-msvc": "1.11.1",
        "@unrs/resolver-binding-win32-ia32-msvc": "1.11.1",
        "@unrs/resolver-binding-win32-x64-msvc": "1.11.1"
      }
    },
    "node_modules/update-browserslist-db": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/update-browserslist-db/-/update-browserslist-db-1.2.3.tgz",
      "integrity": "sha512-Js0m9cx+qOgDxo0eMiFGEueWztz+d4+M3rGlmKPT+T4IS/jP4ylw3Nwpu6cpTTP8R1MAC1kF4VbdLt3ARf209w==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "dependencies": {
        "escalade": "^3.2.0",
        "picocolors": "^1.1.1"
      },
      "bin": {
        "update-browserslist-db": "cli.js"
      },
      "peerDependencies": {
        "browserslist": ">= 4.21.0"
      }
    },
    "node_modules/uri-js": {
      "version": "4.4.1",
      "resolved": "https://registry.npmjs.org/uri-js/-/uri-js-4.4.1.tgz",
      "integrity": "sha512-7rKUyy33Q1yc98pQ1DAmLtwX109F7TIfWlW1Ydo8Wl1ii1SeHieeh0HHfPeL2fMXK6z0s8ecKs9frCuLJvndBg==",
      "dev": true,
      "dependencies": {
        "punycode": "^2.1.0"
      }
    },
    "node_modules/util-deprecate": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/util-deprecate/-/util-deprecate-1.0.2.tgz",
      "integrity": "sha512-EPD5q1uXyFxJpCrLnCc1nHnq3gOa6DZBocAIiI2TaSCA7VCJ1UJDMagCzIkXNsUYfD1daK//LTEQ8xiIbrHtcw==",
      "dev": true
    },
    "node_modules/which": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/which/-/which-2.0.2.tgz",
      "integrity": "sha512-BLI3Tl1TW3Pvl70l3yq3Y64i+awpwXqsGBYWkkqMtnbXgrMD+yj7rhW0kuEDxzJaYXGjEW5ogapKNMEKNMjibA==",
      "dev": true,
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "node-which": "bin/node-which"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/which-boxed-primitive": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/which-boxed-primitive/-/which-boxed-primitive-1.1.1.tgz",
      "integrity": "sha512-TbX3mj8n0odCBFVlY8AxkqcHASw3L60jIuF8jFP78az3C2YhmGvqbHBpAjTRH2/xqYunrJ9g1jSyjCjpoWzIAA==",
      "dev": true,
      "dependencies": {
        "is-bigint": "^1.1.0",
        "is-boolean-object": "^1.2.1",
        "is-number-object": "^1.1.1",
        "is-string": "^1.1.1",
        "is-symbol": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-builtin-type": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/which-builtin-type/-/which-builtin-type-1.2.1.tgz",
      "integrity": "sha512-6iBczoX+kDQ7a3+YJBnh3T+KZRxM/iYNPXicqk66/Qfm1b93iu+yOImkg0zHbj5LNOcNv1TEADiZ0xa34B4q6Q==",
      "dev": true,
      "dependencies": {
        "call-bound": "^1.0.2",
        "function.prototype.name": "^1.1.6",
        "has-tostringtag": "^1.0.2",
        "is-async-function": "^2.0.0",
        "is-date-object": "^1.1.0",
        "is-finalizationregistry": "^1.1.0",
        "is-generator-function": "^1.0.10",
        "is-regex": "^1.2.1",
        "is-weakref": "^1.0.2",
        "isarray": "^2.0.5",
        "which-boxed-primitive": "^1.1.0",
        "which-collection": "^1.0.2",
        "which-typed-array": "^1.1.16"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-collection": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/which-collection/-/which-collection-1.0.2.tgz",
      "integrity": "sha512-K4jVyjnBdgvc86Y6BkaLZEN933SwYOuBFkdmBu9ZfkcAbdVbpITnDmjvZ/aQjRXQrv5EPkTnD1s39GiiqbngCw==",
      "dev": true,
      "dependencies": {
        "is-map": "^2.0.3",
        "is-set": "^2.0.3",
        "is-weakmap": "^2.0.2",
        "is-weakset": "^2.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-typed-array": {
      "version": "1.1.20",
      "resolved": "https://registry.npmjs.org/which-typed-array/-/which-typed-array-1.1.20.tgz",
      "integrity": "sha512-LYfpUkmqwl0h9A2HL09Mms427Q1RZWuOHsukfVcKRq9q95iQxdw0ix1JQrqbcDR9PH1QDwf5Qo8OZb5lksZ8Xg==",
      "dev": true,
      "dependencies": {
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "for-each": "^0.3.5",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/word-wrap": {
      "version": "1.2.5",
      "resolved": "https://registry.npmjs.org/word-wrap/-/word-wrap-1.2.5.tgz",
      "integrity": "sha512-BN22B5eaMMI9UMtjrGd5g5eCYPpCPDUy0FJXbYsaT5zYxjFOckS53SQDE3pWkVoWpHXVb3BrYcEN4Twa55B5cA==",
      "dev": true,
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/yallist": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/yallist/-/yallist-3.1.1.tgz",
      "integrity": "sha512-a4UGQaWPH59mOXUYnAG2ewncQS4i4F43Tv3JoAM+s2VDAmS9NsK8GpDMLrCHPksFT7h3K6TOoUNn2pb7RoXx4g==",
      "dev": true
    },
    "node_modules/yocto-queue": {
      "version": "0.1.0",
      "resolved": "https://registry.npmjs.org/yocto-queue/-/yocto-queue-0.1.0.tgz",
      "integrity": "sha512-rVksvsnNCdJ/ohGc6xgPwyN8eheCxsiLM8mxuE/t/mOVqJewPuO1miLpTHQiRgTKCLexL4MeAFVagts7HmNZ2Q==",
      "dev": true,
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/zod": {
      "version": "4.3.6",
      "resolved": "https://registry.npmjs.org/zod/-/zod-4.3.6.tgz",
      "integrity": "sha512-rftlrkhHZOcjDwkGlnUtZZkvaPHCsDATp4pGpuOOMDaTdDDXF91wuVDJoWoPsKX/3YPQ5fHuF3STjcYyKr+Qhg==",
      "dev": true,
      "funding": {
        "url": "https://github.com/sponsors/colinhacks"
      }
    },
    "node_modules/zod-validation-error": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/zod-validation-error/-/zod-validation-error-4.0.2.tgz",
      "integrity": "sha512-Q6/nZLe6jxuU80qb/4uJ4t5v2VEZ44lzQjPDhYJNztRQ4wyWc6VF3D3Kb/fAuPetZQnhS3hnajCf9CsWesghLQ==",
      "dev": true,
      "engines": {
        "node": ">=18.0.0"
      },
      "peerDependencies": {
        "zod": "^3.25.0 || ^4.0.0"
      }
    }
  }
}

```

### FILE: frontend/package.json
```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint"
  },
  "dependencies": {
    "next": "16.1.6",
    "react": "19.2.3",
    "react-dom": "19.2.3"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "autoprefixer": "^10.4.23",
    "eslint": "^9",
    "eslint-config-next": "16.1.6",
    "postcss": "^8.5.6",
    "tailwindcss": "^3.4.1",
    "typescript": "^5"
  }
}

```

### FILE: frontend/tailwind.config.js
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#020617",
        panel: "#0f172a",
        border: "rgba(255,255,255,0.08)",
        muted: "#94a3b8",
        text: "#e5e7eb",
        good: "#22c55e",
        warn: "#f59e0b",
        bad: "#ef4444",
      },
      borderRadius: {
        xl: "16px",
      },
    },
  },
  plugins: [],
};

```

### FILE: frontend/tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    ".next/types/**/*.ts",
    ".next/dev/types/**/*.ts",
    "**/*.mts"
  ],
  "exclude": ["node_modules"]
}

```

### FILE: pyproject.toml
```toml
[project]
name = "trace-invest"
version = "0.1.0"
description = "Systematic trading & investing engine"
requires-python = ">=3.10"

dependencies = [
    "pandas>=2.1.0",
    "numpy>=1.26.0",
    "pyyaml>=6.0.1",
    "requests>=2.31.0",
    "python-dateutil>=2.9.0",
    "pytz>=2024.1",
    "loguru>=0.7.2",
    "yfinance>=0.2.40",
    "streamlit>=1.31.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "black>=24.1.0",
    "ruff>=0.2.1",
    "mypy>=1.8.0"
]

[tool.black]
line-length = 88
target-version = ["py310"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.10"
ignore_missing_imports = true
strict = false

```

### FILE: src/trace_invest/__init__.py
```py

```

### FILE: src/trace_invest/api/history.py
```py
from fastapi import APIRouter
from trace_invest.memory.reader import load_stock_history

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/{symbol}")
def get_history(symbol: str):
    symbol = symbol.upper()
    history = load_stock_history(symbol)
    history.sort(key=lambda r: r.get("date") or "", reverse=True)
    print("HISTORY LOADED", symbol, len(history))
    return {
        "symbol": symbol,
        "history": history,
    }

```

### FILE: src/trace_invest/config/__init__.py
```py

```

### FILE: src/trace_invest/config/loader.py
```py
from pathlib import Path
import yaml
from typing import Dict, Any

CONFIG_DIR = Path("configs")


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""


def _load_yaml(file_path: Path) -> Dict[str, Any]:
    if not file_path.exists():
        raise ConfigError(f"Missing config file: {file_path.name}")

    with file_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_config() -> Dict[str, Any]:
    """
    Loads and validates all system configuration files.
    This is the single source of truth for the system.
    """
    config_files = [
        "system.yaml",
        "universe.yaml",
        "risk.yaml",
        "data_sources.yaml",
    ]

    config: Dict[str, Any] = {}

    for filename in config_files:
        data = _load_yaml(CONFIG_DIR / filename)
        key = filename.replace(".yaml", "")
        config[key] = data

    _validate_config(config)
    return config


def _validate_config(config: Dict[str, Any]) -> None:
    required_keys = [
        "system",
        "universe",
        "risk",
        "data_sources",
    ]

    for key in required_keys:
        if key not in config or not config[key]:
            raise ConfigError(f"Invalid or empty config section: {key}")


```

### FILE: src/trace_invest/dashboard/app.py
```py
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import sys
import json
from pathlib import Path

# ------------------------------------------------------------------------------
# Path setup
# ------------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from trace_invest.config.loader import load_config
from trace_invest.validation.runner import run_validation
from trace_invest.intelligence.conviction import conviction_score
from trace_invest.outputs.signals import generate_signal
from trace_invest.outputs.journal import create_journal_entry
from trace_invest.dashboard.snapshots import list_snapshots, load_snapshot


# ------------------------------------------------------------------------------
# Helpers (NO UI)
# ------------------------------------------------------------------------------

def load_cached_fundamentals(snapshot_path: Path) -> dict:
    f = snapshot_path / "fundamentals.json"
    return json.loads(f.read_text()) if f.exists() else {}

def latest_snapshot_path():
    base = Path("data/snapshots")
    if not base.exists():
        return None
    snapshots = [p for p in base.iterdir() if p.is_dir()]
    return sorted(snapshots)[-1] if snapshots else None


# ------------------------------------------------------------------------------
# MAIN APP (CALLABLE)
# ------------------------------------------------------------------------------

def run_app():

    st.set_page_config(
        page_title="TRACE MARKETS",
        layout="wide",
    )

    st.title("TRACE MARKETS")
    st.caption("A calm, structured manual for understanding markets")

    # Load config
    config = load_config()
    stocks = config["universe"]["universe"]["stocks"]
    # stocks = json.loads(Path(config["universe"]["universe"]["stocks_file"]).read_text())


    # Load snapshot data
    snap_path = latest_snapshot_path()
    if snap_path is None:
        st.warning("No snapshots available yet. Run the weekly pipeline to generate data.")
        st.stop()

    cached_fundamentals = load_cached_fundamentals(snap_path)

    rows = []
    signals_by_stock = {}
    journals_by_stock = {}

    for stock in stocks:
        name = stock["name"]
        symbol = stock["symbol"]

        processed = cached_fundamentals.get(symbol, {})

        quality = processed.get("quality", {})

        validation = run_validation(
            {
                "financials": processed.get("financials", {}),
                "governance": processed.get("governance", {}),
            }
        )

        conviction = conviction_score(processed, validation)
        signal = generate_signal(conviction)
        journal = create_journal_entry(name, signal)

        signals_by_stock[name] = signal
        journals_by_stock[name] = journal

        rows.append({
            "Stock": name,
            "Conviction": conviction["conviction_score"],
            "Zone": signal["zone"],
            "Risk": conviction["overall_risk"],
            "Confidence": quality.get("confidence", "N/A"), 
        })

    df = pd.DataFrame(rows)

    # --------------------------------------------------------------------------
    # Watchlist Overview
    # --------------------------------------------------------------------------

    st.header("Watchlist Overview")
    st.dataframe(df, use_container_width=True)

    # --------------------------------------------------------------------------
    # Decision Journal
    # --------------------------------------------------------------------------

    st.header("Decision Journal")

    selected_stock = st.selectbox(
        "Select a stock",
        df["Stock"].tolist(),
        key="current_stock_selector",
    )

    st.subheader(f"Decision for {selected_stock}")
    st.json(journals_by_stock[selected_stock])


    st.subheader("Data Quality")

    symbol = next(s["symbol"] for s in stocks if s["name"] == selected_stock)
    q = cached_fundamentals.get(symbol, {}).get("quality", {})

    st.metric("Confidence", q.get("confidence", "N/A"))
    st.json(q)


    # --------------------------------------------------------------------------
    # Snapshot Viewer
    # --------------------------------------------------------------------------

    st.divider()
    st.header("Snapshot Viewer")

    snapshots = list_snapshots()

    if not snapshots:
        st.info("No snapshots found yet. Run the weekly pipeline first.")
        return

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


# ------------------------------------------------------------------------------
# PROD ENTRYPOINT
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    run_app()


```

### FILE: src/trace_invest/dashboard/app_staging.py
```py
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

```

### FILE: src/trace_invest/dashboard/snapshots.py
```py
from pathlib import Path
import json
from typing import List, Dict

SNAPSHOT_DIR = Path("data/snapshots")


def list_snapshots() -> List[Path]:
    if not SNAPSHOT_DIR.exists():
        return []

    dated_dirs = [
        d for d in SNAPSHOT_DIR.iterdir()
        if d.is_dir()
    ]

    if not dated_dirs:
        return []

    latest_dir = sorted(dated_dirs, reverse=True)[0]
    snapshot_file = latest_dir / "snapshot.json"

    if snapshot_file.exists():
        return [snapshot_file]

    return []


def load_snapshot(path: Path) -> Dict:
    return json.loads(path.read_text())

```

### FILE: src/trace_invest/governance/balance_sheet_stress.py
```py
from typing import Dict, List


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def analyze_balance_sheet_stress(processed: Dict) -> Dict:
    balance = processed.get("balance_sheet") or []
    financials = processed.get("financials") or []

    debt_series = _extract_series(balance, "total debt")
    ebitda_series = _extract_series(financials, "ebitda")

    if not debt_series or not ebitda_series:
        return {
            "name": "balance_sheet_stress",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Debt or EBITDA data unavailable",
        }

    years = sorted(
        set(debt_series.keys()) & set(ebitda_series.keys()),
        reverse=True
    )

    if len(years) < 2:
        return {
            "name": "balance_sheet_stress",
            "status": "INSUFFICIENT",
            "risk": "UNKNOWN",
            "explanation": "Less than 2 years of overlapping data",
        }

    latest = years[0]
    oldest = years[-1]

    try:
        debt_change = float(debt_series[latest]) - float(debt_series[oldest])
        ebitda_change = float(ebitda_series[latest]) - float(ebitda_series[oldest])
    except Exception:
        return {
            "name": "balance_sheet_stress",
            "status": "ERROR",
            "risk": "UNKNOWN",
            "explanation": "Unable to compute changes",
        }

    if debt_change <= 0:
        return {
            "name": "balance_sheet_stress",
            "status": "STABLE",
            "risk": "LOW",
            "explanation": "Debt not increasing",
        }

    if debt_change > 0 and ebitda_change > 0:
        return {
            "name": "balance_sheet_stress",
            "status": "MANAGED",
            "risk": "MEDIUM",
            "explanation": "Debt rising but EBITDA also growing",
        }

    return {
        "name": "balance_sheet_stress",
        "status": "STRESSED",
        "risk": "HIGH",
        "explanation": "Debt rising while EBITDA not growing",
    }


```

### FILE: src/trace_invest/governance/capital_allocation.py
```py
from typing import Dict, List


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def analyze_capital_allocation(processed: Dict) -> Dict:
    cashflows = processed.get("cashflow") or []

    fcf_series = _extract_series(cashflows, "free cash flow")
    debt_repay_series = _extract_series(cashflows, "repayment")

    if not fcf_series:
        return {
            "name": "capital_allocation",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Free cash flow data unavailable",
        }

    years = sorted(fcf_series.keys(), reverse=True)

    bad_years = 0

    for y in years:
        try:
            fcf = float(fcf_series.get(y, 0))
            repay = float(debt_repay_series.get(y, 0)) if debt_repay_series else 0
        except Exception:
            continue

        # repayment usually negative when paying debt
        if fcf > 0 and repay > 0:
            bad_years += 1

    if bad_years == 0:
        return {
            "name": "capital_allocation",
            "status": "DISCIPLINED",
            "risk": "LOW",
            "explanation": "Positive FCF not accompanied by rising debt",
        }

    if bad_years == 1:
        return {
            "name": "capital_allocation",
            "status": "QUESTIONABLE",
            "risk": "MEDIUM",
            "explanation": "One year of positive FCF with rising debt",
        }

    return {
        "name": "capital_allocation",
        "status": "POOR",
        "risk": "HIGH",
        "explanation": f"Positive FCF with rising debt in {bad_years} years",
    }


```

### FILE: src/trace_invest/governance/earnings_quality.py
```py
from typing import Dict, List

def _extract_series(rows, target_keywords):
    """
    target_keywords: list of substrings to match against index name
    """
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        index_name = str(row.get("index", "")).lower()

        for kw in target_keywords:
            if kw.lower() in index_name:
                return {
                    k: v
                    for k, v in row.items()
                    if k != "index"
                }

    return {}




def analyze_earnings_quality(processed: Dict) -> Dict:
    financials = processed.get("financials") or []
    cashflows = processed.get("cashflow") or []

    net_income_series = _extract_series(
        financials,
        ["net income", "net profit"]
    )

    cfo_series = _extract_series(
        cashflows,
        [
            "operating cash flow",
            "cash from operating",
            "total cash from operating"
        ]
    )


    common_years = sorted(
        set(net_income_series.keys()) & set(cfo_series.keys()),
        reverse=True
    )

    if not common_years:
        return {
            "name": "earnings_quality",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Net income or operating cash flow history unavailable",
        }

    negative_cfo_positive_profit_years = []

    for y in common_years:
        ni = net_income_series.get(y)
        cfo = cfo_series.get(y)

        if ni is None or cfo is None:
            continue

        if ni > 0 and cfo < 0:
            negative_cfo_positive_profit_years.append(y)

    count = len(negative_cfo_positive_profit_years)

    if count == 0:
        return {
            "name": "earnings_quality",
            "status": "CLEAN",
            "risk": "LOW",
            "explanation": "Operating cash flow aligns with profits",
        }

    if count == 1:
        return {
            "name": "earnings_quality",
            "status": "MINOR_MISMATCH",
            "risk": "MEDIUM",
            "explanation": "One year of positive profit but negative operating cash flow",
        }

    return {
        "name": "earnings_quality",
        "status": "REPEATED_MISMATCH",
        "risk": "HIGH",
        "explanation": f"Profit positive but operating cash flow negative in {count} years",
    }


```

### FILE: src/trace_invest/governance/governance_score.py
```py
from typing import Dict


RISK_POINTS = {
    "LOW": 0,
    "MEDIUM": 2,
    "HIGH": 5,
    "UNKNOWN": 1,
}


def compute_governance_score(details: Dict) -> Dict:
    """
    details: validation["details"]
    """

    total_points = 0
    max_points = 0
    top_risks = []

    for name, result in details.items():
        if name == "fraud":
            continue

        risk = result.get("risk", "UNKNOWN")
        points = RISK_POINTS.get(risk, 1)

        total_points += points
        max_points += 5

        if risk in ("HIGH", "MEDIUM"):
            top_risks.append(
                f"{name}: {result.get('status')}"
            )

    if max_points == 0:
        score = 100
    else:
        score = round(
            100 - (total_points / max_points) * 100
        )

    if score >= 75:
        band = "LOW"
    elif score >= 50:
        band = "MEDIUM"
    else:
        band = "HIGH"

    return {
        "governance_score": score,
        "governance_band": band,
        "top_risks": top_risks,
    }


```

### FILE: src/trace_invest/governance/promoter_pledge.py
```py
from typing import List, Dict


def extract_promoter_pledge(processed: Dict) -> List[Dict]:
    gov = processed.get("governance", {})
    value = gov.get("promoter_pledge_pct")

    if value is None:
        return []

    return [
        {
            "date": "latest",
            "pledge_pct": float(value),
        }
    ]


def analyze_pledge_trend(history: List[Dict]) -> Dict:
    if len(history) == 0:
        return {
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Promoter pledging data not available",
        }

    if len(history) == 1:
        pct = history[0]["pledge_pct"]

        if pct == 0:
            return {
                "status": "NONE",
                "risk": "LOW",
                "explanation": "No promoter pledging",
            }

        if pct < 10:
            return {
                "status": "LOW",
                "risk": "MEDIUM",
                "explanation": "Promoter pledging present but low",
            }

        return {
            "status": "HIGH",
            "risk": "HIGH",
            "explanation": "High promoter pledging",
        }

    # future-proof: trend logic
    values = [h["pledge_pct"] for h in history]
    first = values[0]
    last = values[-1]

    if last > first:
        return {
            "status": "INCREASING",
            "risk": "HIGH",
            "explanation": "Promoter pledging increasing over time",
        }

    if last < first:
        return {
            "status": "DECREASING",
            "risk": "MEDIUM",
            "explanation": "Promoter pledging decreasing",
        }

    return {
        "status": "FLAT",
        "risk": "MEDIUM",
        "explanation": "Promoter pledging stable",
    }

```

### FILE: src/trace_invest/governance/tax_volatility.py
```py
from typing import Dict, List


def _extract_tax_rate_series(rows: List[Dict]) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if "tax rate" in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def analyze_tax_volatility(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    series = _extract_tax_rate_series(financials)

    if not series:
        return {
            "name": "tax_volatility",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Tax rate history unavailable",
        }

    values = []

    for v in series.values():
        try:
            if v is not None:
                values.append(float(v))
        except Exception:
            continue

    if len(values) < 3:
        return {
            "name": "tax_volatility",
            "status": "INSUFFICIENT",
            "risk": "UNKNOWN",
            "explanation": "Less than 3 years of tax rate data",
        }

    min_rate = min(values)
    max_rate = max(values)
    spread = max_rate - min_rate

    if spread < 0.05:
        return {
            "name": "tax_volatility",
            "status": "STABLE",
            "risk": "LOW",
            "explanation": "Tax rate stable across years",
        }

    if spread < 0.15:
        return {
            "name": "tax_volatility",
            "status": "MODERATE",
            "risk": "MEDIUM",
            "explanation": "Moderate variation in tax rate",
        }

    return {
        "name": "tax_volatility",
        "status": "VOLATILE",
        "risk": "HIGH",
        "explanation": "Large swings in effective tax rate",
    }


```

### FILE: src/trace_invest/governance/unusual_items.py
```py
from typing import Dict, List


UNUSUAL_KEYWORDS = [
    "unusual",
    "special",
    "write off",
    "write-off",
    "restructuring",
]


def _extract_unusual_rows(rows: List[Dict]) -> List[Dict]:
    if not isinstance(rows, list):
        return []

    matches = []

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        for kw in UNUSUAL_KEYWORDS:
            if kw in name:
                matches.append(row)
                break

    return matches


def analyze_unusual_items(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    rows = _extract_unusual_rows(financials)

    if not rows:
        return {
            "name": "unusual_items",
            "status": "NONE",
            "risk": "LOW",
            "explanation": "No unusual or special items reported",
        }

    years_with_values = set()

    for row in rows:
        for k, v in row.items():
            if k == "index":
                continue

            try:
                if v and abs(float(v)) > 0:
                    years_with_values.add(k)
            except Exception:
                continue

    count = len(years_with_values)

    if count == 1:
        return {
            "name": "unusual_items",
            "status": "ONE_TIME",
            "risk": "MEDIUM",
            "explanation": "One year shows unusual/special items",
        }

    return {
        "name": "unusual_items",
        "status": "PERSISTENT",
        "risk": "HIGH",
        "explanation": f"Unusual/special items present in {count} years",
    }


```

### FILE: src/trace_invest/ingestion/__init__.py
```py

```

### FILE: src/trace_invest/ingestion/fundamentals.py
```py
from pathlib import Path
from datetime import datetime
import yfinance as yf
import json

from trace_invest.utils.logger import setup_logger

logger = setup_logger()

RAW_DIR = Path("data/raw/fundamentals")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def _df_to_serializable(df):
    """
    Convert pandas DataFrame to JSON-serializable structure.
    """
    if df is None or df.empty:
        return []

    df = df.copy()
    df.columns = [str(c) for c in df.columns]
    df.index = df.index.astype(str)

    return df.reset_index().to_dict(orient="records")


def fetch_fundamentals(symbol: str) -> dict:
    logger.info(f"Fetching fundamentals for {symbol}")
    ticker = yf.Ticker(symbol)

    data = {
        "symbol": symbol,
        "fetched_at": datetime.utcnow().isoformat(),
        "financials": _df_to_serializable(ticker.financials),
        "balance_sheet": _df_to_serializable(ticker.balance_sheet),
        "cashflow": _df_to_serializable(ticker.cashflow),
        "info": ticker.info or {},
    }
    return data



def write_raw_fundamentals(symbol: str, data: dict) -> Path:
    path = RAW_DIR / f"{symbol.replace('.', '_')}.json"
    if path.exists():
        logger.info(f"Raw fundamentals already exist for {symbol}, skipping")
        return path

    path.write_text(json.dumps(data, indent=2))
    logger.info(f"Raw fundamentals written for {symbol}")
    return path


```

### FILE: src/trace_invest/ingestion/prices.py
```py
from datetime import datetime
import json
from pathlib import Path
import pandas as pd
import yfinance as yf

from trace_invest.config.loader import load_config
from trace_invest.utils.logger import setup_logger

logger = setup_logger()

RAW_DATA_DIR = Path("data/raw/prices")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


class PriceIngestionError(Exception):
    pass


def fetch_weekly_prices(symbol: str) -> pd.DataFrame:
    """
    Fetch weekly OHLCV data using Yahoo Finance.
    """
    logger.info(f"Fetching weekly prices for {symbol}")

    ticker = yf.Ticker(symbol)
    df = ticker.history(period="max", interval="1wk", auto_adjust=False)

    if df.empty:
        raise PriceIngestionError(f"No price data returned for {symbol}")

    df.reset_index(inplace=True)
    df["symbol"] = symbol
    df["source"] = "yahoo_finance"
    df["ingested_at"] = datetime.utcnow().isoformat()

    return df


def write_raw_prices(symbol: str, df: pd.DataFrame) -> None:
    file_path = RAW_DATA_DIR / f"{symbol.replace('.', '_')}.csv"

    if file_path.exists():
        logger.warning(f"Raw price file already exists for {symbol}. Skipping write.")
        return

    df.to_csv(file_path, index=False)
    logger.info(f"Raw weekly prices written for {symbol}")


def run_weekly_price_ingestion() -> None:
    config = load_config()
    stocks = config["universe"]["universe"]["stocks"]
    # stocks = json.loads(Path(config["universe"]["universe"]["stocks_file"]).read_text())

    logger.info("Starting weekly price ingestion")

    for stock in stocks:
        symbol = stock["symbol"]
        try:
            df = fetch_weekly_prices(symbol)
            write_raw_prices(symbol, df)
        except Exception as e:
            logger.error(f"Failed to ingest prices for {symbol}: {e}")

    logger.info("Weekly price ingestion completed")

```

### FILE: src/trace_invest/intelligence/__init__.py
```py

```

### FILE: src/trace_invest/intelligence/conviction.py
```py
from typing import Dict

MASTER_POINTS = {
    "ELITE": 35,
    "GOOD": 25,
    "AVERAGE": 15,
    "POOR": 5,
}

GOVERNANCE_POINTS = {
    "LOW": 20,
    "MEDIUM": 10,
    "HIGH": 0,
}

STABILITY_POINTS = {
    "STRONG": 20,
    "AVERAGE": 10,
    "WEAK": 0,
}

VALUATION_POINTS = {
    "REASONABLE": 15,
    "RICH": 8,
    "EXPENSIVE": 0,
    "UNKNOWN": 5,
}

DATA_CONFIDENCE_WEIGHT = 0.1
CONVICTION_MIN = 0
CONVICTION_MAX = 100
CONVICTION_FLOOR = 35


def conviction_score(processed_data: Dict, validation_result: Dict) -> Dict:
    """
    Produces final conviction score (0–100) from banded metrics and data confidence.
    """

    master_band = validation_result.get("master", {}).get("master_band")
    governance_band = validation_result.get("governance", {}).get("governance_band")
    stability_band = validation_result.get("stability", {}).get("stability_band")
    valuation = validation_result.get("details", {}).get("valuation_sanity", {})
    valuation_status = valuation.get("status") if isinstance(valuation, dict) else valuation

    data_confidence_score = validation_result.get("data_confidence_score", 100)
    data_confidence_band = validation_result.get("data_confidence_band", "HIGH")

    master_points = MASTER_POINTS.get(master_band, 0)
    governance_points = GOVERNANCE_POINTS.get(governance_band, 0)
    stability_points = STABILITY_POINTS.get(stability_band, 0)
    valuation_points = VALUATION_POINTS.get(valuation_status, 0)
    confidence_points = round(data_confidence_score * DATA_CONFIDENCE_WEIGHT)

    base_score = (
        master_points
        + governance_points
        + stability_points
        + valuation_points
        + confidence_points
    )

    # Floor protects against over-penalizing when core bands are acceptable.
    if master_band in ("ELITE", "GOOD", "AVERAGE") and governance_band != "HIGH":
        base_score = max(base_score, CONVICTION_FLOOR)

    final_score = max(CONVICTION_MIN, min(CONVICTION_MAX, base_score))

    return {
        "conviction_score": final_score,
        "base_score": base_score,
        "risk_penalty": 0,
        "overall_risk": validation_result.get("overall_risk", "LOW"),
        "data_confidence_score": data_confidence_score,
        "data_confidence_band": data_confidence_band,
        "components": {
            "master_band": master_band,
            "governance_band": governance_band,
            "stability_band": stability_band,
            "valuation_sanity": valuation_status,
            "data_confidence_points": confidence_points,
        },
    }


```

### FILE: src/trace_invest/intelligence/master_score.py
```py
from typing import Dict


def compute_master_score(validation: Dict) -> Dict:
    governance = validation.get("governance", {})
    stability = validation.get("stability", {})
    valuation = validation.get("details", {}).get("valuation_sanity", {})

    g = governance.get("governance_score", 50)
    s = stability.get("stability_score", 50)

    v_risk = valuation.get("risk", "UNKNOWN")

    if v_risk == "LOW":
        v = 80
    elif v_risk == "MEDIUM":
        v = 60
    elif v_risk == "HIGH":
        v = 30
    else:
        v = 50

    score = round((g * 0.4) + (s * 0.4) + (v * 0.2))

    if score >= 75:
        band = "ELITE"
    elif score >= 60:
        band = "GOOD"
    elif score >= 45:
        band = "AVERAGE"
    else:
        band = "POOR"

    return {
        "master_score": score,
        "master_band": band,
    }


```

### FILE: src/trace_invest/intelligence/quality.py
```py
from typing import Dict


def quality_score(metrics: Dict) -> Dict:
    """
    Scores business quality (0–40).
    """

    score = 0
    reasons = []

    roe = metrics.get("roe", 0)
    if roe >= 15:
        score += 15
        reasons.append("Strong ROE")

    debt_to_equity = metrics.get("debt_to_equity", 1)
    if debt_to_equity <= 0.5:
        score += 10
        reasons.append("Low leverage")

    revenue_growth = metrics.get("revenue_growth_5y", 0)
    if revenue_growth >= 10:
        score += 10
        reasons.append("Consistent revenue growth")

    margins = metrics.get("operating_margin", 0)
    if margins >= 15:
        score += 5
        reasons.append("Healthy operating margins")

    return {
        "component": "quality",
        "score": min(score, 40),
        "max_score": 40,
        "reasons": reasons,
    }


```

### FILE: src/trace_invest/intelligence/valuation.py
```py
from typing import Dict


def valuation_score(metrics: Dict) -> Dict:
    """
    Scores valuation attractiveness (0–30).
    """

    score = 0
    reasons = []

    pe = metrics.get("pe_ratio", None)
    if pe is not None:
        if pe <= 15:
            score += 15
            reasons.append("Attractive PE")
        elif pe <= 25:
            score += 8
            reasons.append("Reasonable PE")

    pb = metrics.get("pb_ratio", None)
    if pb is not None and pb <= 3:
        score += 10
        reasons.append("Reasonable PB")

    fcf_yield = metrics.get("fcf_yield", 0)
    if fcf_yield >= 4:
        score += 5
        reasons.append("Healthy free cash flow yield")

    return {
        "component": "valuation",
        "score": min(score, 30),
        "max_score": 30,
        "reasons": reasons,
    }


```

### FILE: src/trace_invest/memory/reader.py
```py
from pathlib import Path
import json
from typing import List


def load_stock_history(symbol: str) -> List[dict]:
    symbol = symbol.upper()
    path = Path("data") / "history" / f"{symbol}.json"
    if not path.exists():
        return []

    try:
        return json.loads(path.read_text())
    except Exception:
        return []

```

### FILE: src/trace_invest/outputs/__init__.py
```py

```

### FILE: src/trace_invest/outputs/history.py
```py
from pathlib import Path
import json
from typing import Dict


HISTORY_DIR = Path("data/history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def update_stock_history(decision: Dict, run_date: str):

    symbol = decision.get("stock")
    v = decision.get("validation", {})

    master = decision.get("master") or v.get("master", {})
    governance = decision.get("governance") or v.get("governance", {})
    stability = decision.get("stability") or v.get("stability", {})
    valuation = decision.get("valuation") or {}
    trend = decision.get("trend") or {}
    details = v.get("details", {})
    val_sanity = valuation.get("valuation_sanity")
    if val_sanity is None:
        val_detail = details.get("valuation_sanity") if isinstance(details, dict) else None
        if isinstance(val_detail, dict):
            val_sanity = val_detail.get("status")
        else:
            val_sanity = val_detail

    row = {
        "date": run_date,
        "decision_zone": decision.get("decision_zone"),
        "master_score": master.get("master_score"),
        "master_band": master.get("master_band"),
        "governance_band": governance.get("governance_band"),
        "stability_band": stability.get("stability_band"),
        "valuation_sanity": val_sanity,
        "overall_risk": decision.get("overall_risk"),
        "trend": trend.get("trend"),
    }

    path = HISTORY_DIR / f"{symbol}.json"

    if path.exists():
        try:
            data = json.loads(path.read_text())
        except Exception:
            data = []
    else:
        data = []

    data.append(row)
    path.write_text(json.dumps(data, indent=2))


```

### FILE: src/trace_invest/outputs/journal.py
```py
from datetime import datetime
from typing import Dict


def create_journal_entry(
    stock_name: str,
    signal: Dict,
) -> Dict:
    """
    Creates a snapshot-ready decision journal entry.
    """

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "stock": stock_name,
        "decision_zone": signal["zone"],
        "conviction_score": signal["conviction_score"],
        "overall_risk": signal["overall_risk"],
        "rationale": {
            "quality": signal["components"]["quality"]["reasons"],
            "valuation": signal["components"]["valuation"]["reasons"],
        },
    }


```

### FILE: src/trace_invest/outputs/narrative.py
```py
from typing import Dict


def generate_narrative(decision: Dict) -> str:
    v = decision.get("validation", {})

    governance = v.get("governance", {})
    stability = v.get("stability", {})
    details = v.get("details", {})

    lines = []

    # --- Business Quality ---
    roe = details.get("median_roe", {})
    margin = details.get("median_operating_margin", {})

    if roe.get("status") in ("EXCELLENT", "GOOD"):
        lines.append("Business shows strong profitability.")
    elif roe.get("status") == "WEAK":
        lines.append("Business profitability is weak.")

    if margin.get("status") in ("EXCELLENT", "GOOD"):
        lines.append("Operating margins are healthy.")
    elif margin.get("status") == "WEAK":
        lines.append("Operating margins are thin.")

    # --- Governance ---
    gov_band = governance.get("governance_band")

    if gov_band == "LOW":
        lines.append("No major governance red flags detected.")
    elif gov_band == "MEDIUM":
        lines.append("Some governance concerns exist.")
    else:
        lines.append("High governance risk detected.")

    for risk in governance.get("top_risks", []):
        lines.append(f"Key issue: {risk.replace('_', ' ')}.")

    # --- Stability ---
    stab_band = stability.get("stability_band")

    if stab_band == "STRONG":
        lines.append("Business performance is stable across years.")
    elif stab_band == "AVERAGE":
        lines.append("Business shows mixed stability.")
    else:
        lines.append("Business shows unstable or weakening trends.")

    for weak in stability.get("weak_areas", []):
        lines.append(f"Weak area: {weak.replace('_', ' ')}.")

    # --- Valuation ---
    valuation = details.get("valuation_sanity", {})
    val_status = valuation.get("status")

    if val_status == "REASONABLE":
        lines.append("Valuation appears reasonable.")
    elif val_status == "RICH":
        lines.append("Valuation looks stretched.")
    elif val_status == "EXPENSIVE":
        lines.append("Valuation is expensive.")

    return " ".join(lines)


```

### FILE: src/trace_invest/outputs/rankings.py
```py
from typing import List, Dict


def _top_n(items: List[Dict], key: str, n=30, reverse=True):
    return sorted(
        items,
        key=lambda x: x.get(key, 0),
        reverse=reverse
    )[:n]


def generate_rankings(decisions: List[Dict]) -> Dict:

    rows = []

    for d in decisions:
        v = d.get("validation", {})
        master = v.get("master", {})
        governance = v.get("governance", {})
        stability = v.get("stability", {})
        trend = d.get("trend", {})

        rows.append({
            "symbol": d.get("stock"),
            "master_score": master.get("master_score", 0),
            "master_band": master.get("master_band"),
            "governance_band": governance.get("governance_band"),
            "stability_band": stability.get("stability_band"),
            "trend": trend.get("trend"),
            "trend_delta": trend.get("delta"),
        })

    return {
        "top_master": _top_n(rows, "master_score", 30, True),
        "bottom_master": _top_n(rows, "master_score", 30, False),
        "low_governance": [r for r in rows if r["governance_band"] == "LOW"][:30],
        "strong_stability": [r for r in rows if r["stability_band"] == "STRONG"][:30],
        "top_improving": [
            r for r in rows if r["trend"] == "IMPROVING"
        ][:30],
        "top_deteriorating": [
            r for r in rows if r["trend"] == "DETERIORATING"
        ][:30],
    }


```

### FILE: src/trace_invest/outputs/sector_trends.py
```py
from typing import Dict, List
from collections import defaultdict


def generate_sector_trends(decisions: List[Dict], universe: List[Dict]) -> Dict:

    symbol_to_sector = {
        s["symbol"]: s.get("sector", "UNKNOWN")
        for s in universe
    }

    buckets = defaultdict(list)

    for d in decisions:
        sector = symbol_to_sector.get(d.get("stock"), "UNKNOWN")
        trend = d.get("trend", {})
        delta = trend.get("delta")

        if delta is not None:
            buckets[sector].append(delta)

    output = {}

    for sector, deltas in buckets.items():

        if not deltas:
            avg = None
        else:
            avg = round(sum(deltas) / len(deltas), 2)

        if avg is None:
            label = "NO_DATA"
        elif avg >= 3:
            label = "IMPROVING"
        elif avg <= -3:
            label = "DETERIORATING"
        else:
            label = "STABLE"

        output[sector] = {
            "avg_trend_delta": avg,
            "trend": label,
            "count": len(deltas),
        }

    return output


```

### FILE: src/trace_invest/outputs/sectors.py
```py
from typing import Dict, List
from collections import defaultdict


def generate_sector_summary(decisions: List[Dict], universe: List[Dict]) -> Dict:

    symbol_to_sector = {
        s["symbol"]: s.get("sector", "UNKNOWN")
        for s in universe
    }

    buckets = defaultdict(list)

    for d in decisions:
        sector = symbol_to_sector.get(d.get("stock"), "UNKNOWN")
        buckets[sector].append(d)

    output = {}

    for sector, rows in buckets.items():

        master_scores = []
        low_gov = 0
        strong_stab = 0

        for d in rows:
            v = d.get("validation", {})
            master = v.get("master", {})
            governance = v.get("governance", {})
            stability = v.get("stability", {})

            if master.get("master_score") is not None:
                master_scores.append(master.get("master_score"))

            if governance.get("governance_band") == "LOW":
                low_gov += 1

            if stability.get("stability_band") == "STRONG":
                strong_stab += 1

        count = len(rows)

        output[sector] = {
            "count": count,
            "avg_master_score": round(sum(master_scores) / len(master_scores), 1)
            if master_scores else None,
            "low_governance_pct": round(low_gov / count * 100, 1),
            "strong_stability_pct": round(strong_stab / count * 100, 1),
        }

    return output


```

### FILE: src/trace_invest/outputs/signals.py
```py
from typing import Dict


def conviction_to_zone(conviction_score: int) -> str:
    if conviction_score >= 75:
        return "BUY"
    if conviction_score >= 55:
        return "HOLD"
    if conviction_score >= 35:
        return "REDUCE"
    return "EXIT"


def generate_signal(conviction_result: Dict) -> Dict:
    score = conviction_result["conviction_score"]
    zone = conviction_to_zone(score)

    if conviction_result.get("data_confidence_band") == "LOW" and zone in ("EXIT", "REDUCE"):
        zone = "HOLD"

    return {
        "conviction_score": score,
        "zone": zone,
        "overall_risk": conviction_result["overall_risk"],
        "components": conviction_result["components"],
        "risk_penalty": conviction_result["risk_penalty"],
    }


```

### FILE: src/trace_invest/outputs/trends.py
```py
from pathlib import Path
import json
from typing import Dict, List

HISTORY_DIR = Path("data/history")


def compute_trend(symbol: str) -> Dict:
    path = HISTORY_DIR / f"{symbol}.json"

    if not path.exists():
        return {
            "trend": "NO_DATA",
            "delta": None,
        }

    try:
        data = json.loads(path.read_text())
    except Exception:
        return {
            "trend": "NO_DATA",
            "delta": None,
        }

    if len(data) < 2:
        return {
            "trend": "NO_DATA",
            "delta": None,
        }

    window = data[-4:]  # last 4 entries

    first = window[0].get("master_score")
    last = window[-1].get("master_score")

    if first is None or last is None:
        return {
            "trend": "NO_DATA",
            "delta": None,
        }

    delta = round(last - first, 1)

    if delta >= 5:
        label = "IMPROVING"
    elif delta <= -5:
        label = "DETERIORATING"
    else:
        label = "STABLE"

    return {
        "trend": label,
        "delta": delta,
    }


```

### FILE: src/trace_invest/outputs/watchlist.py
```py
from typing import List, Dict


def generate_long_term_watchlist(decisions: List[Dict]) -> Dict:

    core = []
    candidates = []
    watch = []

    for d in decisions:
        v = d.get("validation", {})

        master = v.get("master", {})
        governance = v.get("governance", {})
        stability = v.get("stability", {})

        master_band = master.get("master_band")
        gov_band = governance.get("governance_band")
        stab_band = stability.get("stability_band")

        row = {
            "symbol": d.get("stock"),
            "master_score": master.get("master_score"),
        }

        # CORE
        if (
            master_band == "ELITE"
            and gov_band == "LOW"
            and stab_band == "STRONG"
        ):
            core.append(row)

        # CANDIDATES
        elif (
            master_band == "GOOD"
            and gov_band == "LOW"
            and stab_band in ("STRONG", "AVERAGE")
        ):
            candidates.append(row)

        # WATCH
        elif (
            master_band == "AVERAGE"
            and gov_band == "LOW"
        ):
            watch.append(row)

    return {
        "core": core,
        "candidates": candidates,
        "watch": watch,
    }


```

### FILE: src/trace_invest/pipeline/__init__.py
```py

```

### FILE: src/trace_invest/pipeline/delta.py
```py
from __future__ import annotations

from typing import Dict, List, Optional, Tuple


ZONE_ORDER = {
    "BUY": 3,
    "HOLD": 2,
    "REDUCE": 1,
    "EXIT": 0,
}

RISK_ORDER = {
    "LOW": 0,
    "MEDIUM": 1,
    "HIGH": 2,
    "UNKNOWN": 1,
}

MASTER_ORDER = {
    "ELITE": 3,
    "GOOD": 2,
    "AVERAGE": 1,
    "POOR": 0,
}

GOVERNANCE_ORDER = {
    "LOW": 2,
    "MEDIUM": 1,
    "HIGH": 0,
}

STABILITY_ORDER = {
    "STRONG": 2,
    "AVERAGE": 1,
    "WEAK": 0,
}

VALUATION_ORDER = {
    "REASONABLE": 2,
    "RICH": 1,
    "EXPENSIVE": 0,
    "UNKNOWN": 1,
}


def build_snapshot_deltas(
    decisions: List[Dict],
    previous_snapshot: Optional[Dict],
) -> Tuple[List[Dict], Dict]:
    prev_map = {}
    if previous_snapshot:
        for prev in previous_snapshot.get("decisions", []):
            if isinstance(prev, dict) and prev.get("stock"):
                prev_map[prev["stock"]] = prev

    stats = {
        "upgrades": 0,
        "downgrades": 0,
        "decision_zone_changes": 0,
        "risk_increases": 0,
        "risk_decreases": 0,
        "band_shifts": {
            "master": {"improved": 0, "worsened": 0},
            "governance": {"improved": 0, "worsened": 0},
            "stability": {"improved": 0, "worsened": 0},
            "valuation": {"improved": 0, "worsened": 0},
        },
    }

    for decision in decisions:
        prev = prev_map.get(decision.get("stock"))
        delta = build_stock_delta(decision, prev)
        decision["delta"] = delta

        if delta.get("decision_change") == "UPGRADE":
            stats["upgrades"] += 1
        elif delta.get("decision_change") == "DOWNGRADE":
            stats["downgrades"] += 1

        if delta.get("decision_change") in ("UPGRADE", "DOWNGRADE"):
            stats["decision_zone_changes"] += 1

        if delta.get("risk_change") == "INCREASE":
            stats["risk_increases"] += 1
        elif delta.get("risk_change") == "DECREASE":
            stats["risk_decreases"] += 1

        for band_key in ("master", "governance", "stability", "valuation"):
            change = delta.get("band_changes", {}).get(band_key)
            if change == "IMPROVED":
                stats["band_shifts"][band_key]["improved"] += 1
            elif change == "WORSENED":
                stats["band_shifts"][band_key]["worsened"] += 1

    return decisions, stats


def build_stock_delta(current: Dict, previous: Optional[Dict]) -> Dict:
    if not previous:
        return {
            "from_previous": None,
            "changes": ["Initial snapshot"],
            "change_summary": "Initial snapshot",
            "decision_change": "UNCHANGED",
            "risk_change": "UNCHANGED",
            "band_changes": {},
        }

    changes: List[str] = []
    band_changes: Dict[str, str] = {}

    prev_zone = previous.get("decision_zone")
    curr_zone = current.get("decision_zone")
    decision_change = _compare_ordered(prev_zone, curr_zone, ZONE_ORDER)

    if prev_zone != curr_zone:
        changes.append(f"Decision zone changed from {prev_zone} to {curr_zone}.")

    prev_risk = previous.get("overall_risk")
    curr_risk = current.get("overall_risk")
    risk_change = _compare_ordered(prev_risk, curr_risk, RISK_ORDER)

    if prev_risk != curr_risk:
        verb = "increased" if risk_change == "INCREASE" else "decreased"
        changes.append(f"Overall risk {verb} from {prev_risk} to {curr_risk}.")

    changes, band_changes = _compare_band(
        changes,
        band_changes,
        "master",
        _nested(previous, ("master", "master_band")),
        _nested(current, ("master", "master_band")),
        MASTER_ORDER,
        "Master band",
    )

    changes, band_changes = _compare_band(
        changes,
        band_changes,
        "governance",
        _nested(previous, ("governance", "governance_band")),
        _nested(current, ("governance", "governance_band")),
        GOVERNANCE_ORDER,
        "Governance band",
    )

    changes, band_changes = _compare_band(
        changes,
        band_changes,
        "stability",
        _nested(previous, ("stability", "stability_band")),
        _nested(current, ("stability", "stability_band")),
        STABILITY_ORDER,
        "Stability band",
    )

    changes, band_changes = _compare_band(
        changes,
        band_changes,
        "valuation",
        _nested(previous, ("valuation", "valuation_sanity")),
        _nested(current, ("valuation", "valuation_sanity")),
        VALUATION_ORDER,
        "Valuation sanity",
    )

    if not changes:
        changes = ["No material changes"]

    return {
        "from_previous": {
            "decision_zone": prev_zone,
            "overall_risk": prev_risk,
            "master_band": _nested(previous, ("master", "master_band")),
            "governance_band": _nested(previous, ("governance", "governance_band")),
            "stability_band": _nested(previous, ("stability", "stability_band")),
            "valuation_sanity": _nested(previous, ("valuation", "valuation_sanity")),
        },
        "changes": changes,
        "change_summary": " ".join(changes),
        "decision_change": decision_change,
        "risk_change": risk_change,
        "band_changes": band_changes,
    }


def _compare_ordered(prev: Optional[str], curr: Optional[str], order: Dict[str, int]) -> str:
    prev_val = order.get(prev or "", 0)
    curr_val = order.get(curr or "", 0)

    if curr_val > prev_val:
        return "UPGRADE" if order is ZONE_ORDER else "INCREASE"
    if curr_val < prev_val:
        return "DOWNGRADE" if order is ZONE_ORDER else "DECREASE"
    return "UNCHANGED"


def _compare_band(
    changes: List[str],
    band_changes: Dict[str, str],
    key: str,
    prev: Optional[str],
    curr: Optional[str],
    order: Dict[str, int],
    label: str,
) -> Tuple[List[str], Dict[str, str]]:
    if prev == curr:
        return changes, band_changes

    prev_val = order.get(prev or "", 0)
    curr_val = order.get(curr or "", 0)

    if curr_val > prev_val:
        band_changes[key] = "IMPROVED"
        verb = "improved"
    else:
        band_changes[key] = "WORSENED"
        verb = "weakened"

    changes.append(f"{label} {verb} from {prev} to {curr}.")
    return changes, band_changes


def _nested(obj: Dict, path: Tuple[str, ...]) -> Optional[str]:
    current = obj
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current

```

### FILE: src/trace_invest/pipeline/market_summary.py
```py
from __future__ import annotations

from typing import Dict, List


def generate_market_summary(decisions: List[Dict], delta_stats: Dict) -> Dict:
    summary = {
        "total_stocks": len(decisions),
        "by_decision_zone": {},
        "by_overall_risk": {},
        "upgrades": delta_stats.get("upgrades", 0),
        "downgrades": delta_stats.get("downgrades", 0),
        "risk_increases": delta_stats.get("risk_increases", 0),
        "risk_decreases": delta_stats.get("risk_decreases", 0),
        "band_shifts": delta_stats.get("band_shifts", {}),
    }

    for decision in decisions:
        zone = decision.get("decision_zone")
        risk = decision.get("overall_risk")

        summary["by_decision_zone"][zone] = (
            summary["by_decision_zone"].get(zone, 0) + 1
        )

        summary["by_overall_risk"][risk] = (
            summary["by_overall_risk"].get(risk, 0) + 1
        )

    summary["market_tone"] = _market_tone(summary)
    return summary


def _market_tone(summary: Dict) -> str:
    total = summary.get("total_stocks", 0) or 0
    upgrades = summary.get("upgrades", 0)
    downgrades = summary.get("downgrades", 0)
    high_risk = summary.get("by_overall_risk", {}).get("HIGH", 0)

    if total == 0:
        return "NO_DATA"

    high_ratio = high_risk / total

    if upgrades > downgrades and high_ratio <= 0.2:
        return "CONSTRUCTIVE"
    if downgrades > upgrades or high_ratio >= 0.4:
        return "CAUTIOUS"
    return "MIXED"

```

### FILE: src/trace_invest/pipeline/reasoning_story.py
```py
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

SNAPSHOT_VERSION = "v1"

GOVERNANCE_KEYS = {
    "earnings_quality",
    "unusual_items",
    "tax_volatility",
    "capital_allocation",
    "balance_sheet_stress",
}

STABILITY_KEYS = {
    "median_roe",
    "median_operating_margin",
    "revenue_cagr",
    "fcf_cagr",
    "consistency",
}

VALUATION_KEYS = {
    "valuation_sanity",
}

FRAUD_KEYS = {
    "fraud",
}


def build_reasoning_story(decision: Dict, snapshot_meta: Dict) -> Dict:
    validation = decision.get("validation", {})
    details = validation.get("details", {})

    facts = _group_facts(details)
    interpretation = _interpretation_rules(decision, validation)
    aggregation = _aggregation_logic(decision, validation)
    delta = _delta_interpretation(decision.get("delta", {}))
    verdict = _final_verdict(decision, validation)

    return {
        "metadata": {
            "stock": decision.get("stock"),
            "symbol": decision.get("symbol"),
            "run_date": snapshot_meta.get("run_date"),
            "snapshot_version": snapshot_meta.get("schema_version", SNAPSHOT_VERSION),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "evaluation_scope": {
            "categories": [
                "governance",
                "stability",
                "valuation",
                "fraud",
            ]
        },
        "observed_facts": facts,
        "interpretation_rules": interpretation,
        "aggregation_logic": aggregation,
        "delta_interpretation": delta,
        "final_verdict": verdict,
        "verification_guidance": _verification_guidance(),
    }


def reasoning_story_filename(decision: Dict) -> str:
    symbol = decision.get("symbol")
    if symbol:
        base = symbol.replace(".", "_")
    else:
        base = str(decision.get("stock") or "UNKNOWN").replace(" ", "_")

    cleaned = "".join(ch for ch in base.upper() if ch.isalnum() or ch == "_")
    return f"{cleaned}.json"


def _group_facts(details: Dict) -> Dict:
    grouped = {
        "governance": [],
        "stability": [],
        "valuation": [],
        "fraud": [],
        "other": [],
    }

    for key, value in details.items():
        fact = _fact_from_detail(key, value)
        if key in GOVERNANCE_KEYS:
            grouped["governance"].append(fact)
        elif key in STABILITY_KEYS:
            grouped["stability"].append(fact)
        elif key in VALUATION_KEYS:
            grouped["valuation"].append(fact)
        elif key in FRAUD_KEYS:
            grouped["fraud"].append(fact)
        else:
            grouped["other"].append(fact)

    return grouped


def _fact_from_detail(name: str, detail: Dict) -> Dict:
    return {
        "name": name,
        "status": detail.get("status"),
        "risk": detail.get("risk") or detail.get("risk_level"),
        "explanation": detail.get("explanation"),
    }


def _interpretation_rules(decision: Dict, validation: Dict) -> List[Dict]:
    governance = validation.get("governance", {})
    stability = validation.get("stability", {})
    master = validation.get("master", {})
    conviction_score = decision.get("conviction_score")
    overall_risk = validation.get("overall_risk")

    return [
        {
            "rule_id": "governance_band_thresholds",
            "statement": "Governance band is derived from governance score thresholds.",
            "inputs": {"governance_score": governance.get("governance_score")},
            "result": {"governance_band": governance.get("governance_band")},
        },
        {
            "rule_id": "stability_band_thresholds",
            "statement": "Stability band is derived from stability score thresholds.",
            "inputs": {"stability_score": stability.get("stability_score")},
            "result": {"stability_band": stability.get("stability_band")},
        },
        {
            "rule_id": "master_band_thresholds",
            "statement": "Master band aggregates governance, stability, and valuation sanity.",
            "inputs": {"master_score": master.get("master_score")},
            "result": {"master_band": master.get("master_band")},
        },
        {
            "rule_id": "overall_risk_from_flags",
            "statement": "Overall risk is derived from total flags across validation checks.",
            "inputs": {"total_flags": validation.get("total_flags")},
            "result": {"overall_risk": overall_risk},
        },
        {
            "rule_id": "decision_zone_from_conviction",
            "statement": "Decision zone is derived from conviction score thresholds.",
            "inputs": {"conviction_score": conviction_score},
            "result": {"decision_zone": decision.get("decision_zone")},
        },
    ]


def _aggregation_logic(decision: Dict, validation: Dict) -> Dict:
    governance = validation.get("governance", {})
    stability = validation.get("stability", {})
    master = validation.get("master", {})

    return {
        "governance_band": {
            "score": governance.get("governance_score"),
            "band": governance.get("governance_band"),
            "thresholds": {
                "LOW": ">= 75",
                "MEDIUM": ">= 50",
                "HIGH": "< 50",
            },
        },
        "stability_band": {
            "score": stability.get("stability_score"),
            "band": stability.get("stability_band"),
            "thresholds": {
                "STRONG": ">= 75",
                "AVERAGE": ">= 50",
                "WEAK": "< 50",
            },
        },
        "master_band": {
            "score": master.get("master_score"),
            "band": master.get("master_band"),
            "thresholds": {
                "ELITE": ">= 75",
                "GOOD": ">= 60",
                "AVERAGE": ">= 45",
                "POOR": "< 45",
            },
        },
        "overall_risk": {
            "total_flags": validation.get("total_flags"),
            "thresholds": {
                "LOW": "0",
                "MEDIUM": "1-3",
                "HIGH": ">= 4",
            },
        },
        "decision_zone": {
            "conviction_score": decision.get("conviction_score"),
            "thresholds": {
                "BUY": ">= 75",
                "HOLD": ">= 55",
                "REDUCE": ">= 35",
                "EXIT": "< 35",
            },
        },
    }


def _delta_interpretation(delta: Dict) -> Dict:
    decision_change = delta.get("decision_change")
    risk_change = delta.get("risk_change")

    impact = "NONE"
    if decision_change and decision_change != "UNCHANGED":
        impact = "VERDICT_CHANGED"
    elif risk_change and risk_change != "UNCHANGED":
        impact = "RISK_CHANGED"

    return {
        "change_summary": delta.get("change_summary"),
        "changes": delta.get("changes", []),
        "decision_change": decision_change,
        "risk_change": risk_change,
        "band_changes": delta.get("band_changes", {}),
        "verdict_impact": impact,
    }


def _final_verdict(decision: Dict, validation: Dict) -> Dict:
    governance = validation.get("governance", {})
    stability = validation.get("stability", {})
    valuation = validation.get("details", {}).get("valuation_sanity", {})

    reasons: List[str] = []
    for risk in governance.get("top_risks", [])[:3]:
        reasons.append(f"Governance issue: {risk}")

    for weak in stability.get("weak_areas", [])[:3]:
        reasons.append(f"Stability issue: {weak}")

    valuation_status = None
    if isinstance(valuation, dict):
        valuation_status = valuation.get("status")
    else:
        valuation_status = valuation

    if valuation_status and valuation_status != "REASONABLE":
        reasons.append(f"Valuation sanity: {valuation_status}")

    if not reasons:
        reasons.append("No material issues detected in rule checks")

    uncertainties = _uncertainties(validation.get("details", {}))

    return {
        "decision_zone": decision.get("decision_zone"),
        "overall_risk": decision.get("overall_risk"),
        "primary_reasons": reasons,
        "uncertainties": uncertainties,
    }


def _uncertainties(details: Dict) -> List[str]:
    items = []

    for name, detail in details.items():
        status = detail.get("status")
        risk = detail.get("risk") or detail.get("risk_level")
        if status in ("NO_DATA", "UNKNOWN") or risk in ("UNKNOWN", None):
            items.append(name)

    return sorted(set(items))


def _verification_guidance() -> List[str]:
    return [
        "Review multi-year income statements for revenue and margin trends.",
        "Verify operating cash flow aligns with reported profits.",
        "Check balance sheet leverage and debt movement over time.",
        "Inspect unusual or special items in the notes to accounts.",
        "Review tax rate history for volatility or anomalies.",
    ]

```

### FILE: src/trace_invest/pipeline/snapshot_builder.py
```py
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional

from zoneinfo import ZoneInfo

from trace_invest.config.loader import load_config
from trace_invest.processing.fundamentals import build_processed_fundamentals
from trace_invest.validation.runner import run_validation
from trace_invest.validation.system_awareness import build_system_awareness
from trace_invest.intelligence.conviction import conviction_score
from trace_invest.outputs.signals import generate_signal
from trace_invest.outputs.narrative import generate_narrative
from trace_invest.quality.coverage import coverage_score
from trace_invest.quality.freshness import freshness_score
from trace_invest.quality.confidence import confidence_band
from trace_invest.utils.logger import setup_logger

from trace_invest.pipeline.delta import build_snapshot_deltas
from trace_invest.pipeline.market_summary import generate_market_summary
from trace_invest.pipeline.reasoning_story import (
    build_reasoning_story,
    reasoning_story_filename,
)


SNAPSHOT_SCHEMA_VERSION = "v1"
RAW_DIR = Path("data/raw/fundamentals")
SNAPSHOT_ROOT = Path("data/snapshots")
CONFIG_DIR = Path("configs")


logger = setup_logger()


def build_snapshot(run_date: Optional[str] = None) -> Dict:
    config = load_config()
    run_date = run_date or _today_in_timezone(config)

    snapshot_dir = SNAPSHOT_ROOT / run_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    run_timestamp = datetime.now(timezone.utc).isoformat()

    decisions = _build_decisions(config)
    decisions = sorted(decisions, key=lambda d: (d.get("stock") or "").upper())

    previous_snapshot = _load_previous_snapshot(run_date)
    decisions, delta_stats = build_snapshot_deltas(decisions, previous_snapshot)

    snapshot = {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "run_date": run_date,
        "run_timestamp": run_timestamp,
        "decisions": decisions,
    }

    market_summary = generate_market_summary(decisions, delta_stats)
    metadata = _build_metadata(run_date, run_timestamp, decisions)

    _write_reasoning_stories(snapshot_dir, snapshot, decisions)

    _write_json(snapshot_dir / "snapshot.json", snapshot)
    _write_json(snapshot_dir / "market_summary.json", market_summary)
    _write_json(snapshot_dir / "metadata.json", metadata)

    return {
        "snapshot": snapshot,
        "market_summary": market_summary,
        "metadata": metadata,
    }


def _write_reasoning_stories(snapshot_dir: Path, snapshot: Dict, decisions: List[Dict]) -> None:
    reasoning_dir = snapshot_dir / "reasoning"
    reasoning_dir.mkdir(parents=True, exist_ok=True)

    for decision in decisions:
        story = build_reasoning_story(decision, snapshot)
        filename = reasoning_story_filename(decision)
        _write_json(reasoning_dir / filename, story)


def _build_decisions(config: Dict) -> List[Dict]:
    universe = _load_universe(config)
    decisions: List[Dict] = []

    for stock in universe:
        name = stock.get("name")
        symbol = stock.get("symbol")
        if not symbol:
            logger.warning("Skipping stock with missing symbol: {}", stock)
            continue

        raw = _load_raw_fundamentals(symbol)
        if not raw:
            logger.warning("Missing raw fundamentals for {}", symbol)
            continue

        processed = build_processed_fundamentals(raw)
        coverage = coverage_score(processed)
        freshness = freshness_score(coverage.get("years", []))
        confidence = confidence_band(coverage, freshness)

        validation = run_validation(processed)
        conviction = conviction_score(processed, validation)
        signal = generate_signal(conviction)

        narrative = generate_narrative({"validation": validation})
        valuation_sanity = _extract_valuation_status(validation)

        decision = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "stock": name or symbol,
            "symbol": symbol,
            "decision_zone": signal.get("zone"),
            "conviction_score": int(round(signal.get("conviction_score", 0))),
            "overall_risk": validation.get("overall_risk"),
            "data_confidence_score": validation.get("data_confidence_score"),
            "data_confidence_band": validation.get("data_confidence_band"),
            "narrative": narrative,
            "master": validation.get("master"),
            "governance": validation.get("governance"),
            "stability": validation.get("stability"),
            "valuation": {
                "valuation_sanity": valuation_sanity,
            },
            "quality": {
                "confidence_band": confidence,
            },
            "trend": {
                "trend": "NO_DATA",
                "delta": None,
            },
            "validation": validation,
        }

        decision["system_awareness"] = build_system_awareness(decision, validation)

        decisions.append(decision)

    return decisions


def _load_universe(config: Dict) -> List[Dict]:
    universe = config.get("universe", {}).get("universe", {})
    stocks = universe.get("stocks") or []

    if stocks:
        return stocks

    stocks_file = universe.get("stocks_file")
    if not stocks_file:
        return []

    path = Path(stocks_file)
    if not path.exists():
        logger.warning("Universe stocks_file not found: {}", path)
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Failed to read universe file {}: {}", path, exc)
        return []

    return data if isinstance(data, list) else []


def _load_raw_fundamentals(symbol: str) -> Optional[Dict]:
    filename = f"{symbol.replace('.', '_').upper()}.json"
    path = RAW_DIR / filename

    if not path.exists():
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Failed to read raw fundamentals {}: {}", path, exc)
        return None


def _load_previous_snapshot(run_date: str) -> Optional[Dict]:
    if not SNAPSHOT_ROOT.exists():
        return None

    dates = [
        d.name for d in SNAPSHOT_ROOT.iterdir()
        if d.is_dir()
    ]

    previous_dates = sorted(d for d in dates if d < run_date)
    if not previous_dates:
        return None

    previous_dir = SNAPSHOT_ROOT / previous_dates[-1]
    snapshot_file = previous_dir / "snapshot.json"
    if not snapshot_file.exists():
        return None

    try:
        return json.loads(snapshot_file.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Failed to load previous snapshot {}: {}", snapshot_file, exc)
        return None


def _extract_valuation_status(validation: Dict) -> Optional[str]:
    valuation = validation.get("details", {}).get("valuation_sanity")
    if isinstance(valuation, dict):
        return valuation.get("status")
    return valuation


def _today_in_timezone(config: Dict) -> str:
    tz_name = config.get("system", {}).get("timezone", "UTC")
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = timezone.utc

    return datetime.now(tz).date().isoformat()


def _write_json(path: Path, payload: Dict) -> None:
    path.write_text(
        json.dumps(_sanitize(payload), indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _sanitize(obj):
    if isinstance(obj, float):
        if obj != obj or obj in (float("inf"), float("-inf")):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


def _build_metadata(run_date: str, run_timestamp: str, decisions: List[Dict]) -> Dict:
    config_files = [
        "system.yaml",
        "universe.yaml",
        "risk.yaml",
        "data_sources.yaml",
    ]

    configs = []
    for filename in config_files:
        path = CONFIG_DIR / filename
        if path.exists():
            configs.append({
                "path": str(path).replace("\\", "/"),
                "sha256": _hash_file(path),
            })

    inputs = []
    for decision in decisions:
        symbol = decision.get("symbol")
        if not symbol:
            continue
        filename = f"{symbol.replace('.', '_').upper()}.json"
        path = RAW_DIR / filename
        if path.exists():
            inputs.append({
                "path": str(path).replace("\\", "/"),
                "sha256": _hash_file(path),
            })

    return {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "run_date": run_date,
        "run_timestamp": run_timestamp,
        "config_files": configs,
        "input_files": inputs,
    }


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

```

### FILE: src/trace_invest/portfolio/engine.py
```py
from typing import Dict


MAX_POSITIONS = 15
BASE_POSITION_PCT = 0.05   # 5%
MAX_POSITION_PCT = 0.10    # 10%


def evaluate_portfolio_action(
    portfolio: Dict,
    decision: Dict
) -> Dict:

    symbol = decision.get("stock")
    entry_filter = decision.get("entry_filter", {})
    decision_zone = decision.get("decision_zone")

    capital = portfolio["capital"]
    cash = portfolio["cash"]
    positions = portfolio["positions"]

    target_position_value = capital * BASE_POSITION_PCT

    # -----------------------------
    # BUY LOGIC
    # -----------------------------
    if (
        decision_zone == "ACCUMULATE"
        and entry_filter.get("entry_allowed")
        and symbol not in positions
        and len(positions) < MAX_POSITIONS
        and cash >= target_position_value
    ):
        return {
            "action": "BUY",
            "symbol": symbol,
            "amount": round(target_position_value)
        }

    # -----------------------------
    # SELL LOGIC
    # -----------------------------
    if decision_zone == "EXIT" and symbol in positions:
        return {
            "action": "SELL",
            "symbol": symbol,
            "amount": positions[symbol]["value"]
        }

    return {
        "action": "HOLD",
        "symbol": symbol
    }


```

### FILE: src/trace_invest/portfolio/exit_manager.py
```py
from typing import Dict


def evaluate_exit_override(decision: Dict) -> Dict:

    v = decision.get("validation", {})
    master = v.get("master", {})
    governance = v.get("governance", {})
    trend = decision.get("trend", {})
    tech = decision.get("technical_score", {})

    master_band = master.get("master_band")
    gov_band = governance.get("governance_band")
    trend_label = trend.get("trend")
    tech_band = tech.get("technical_band")

    should_exit = (
        master_band == "POOR"
        or gov_band == "HIGH"
        or (trend_label == "DETERIORATING" and tech_band == "WEAK")
    )

    return {
        "exit_override": should_exit,
        "reasons": {
            "master_band": master_band,
            "governance_band": gov_band,
            "trend": trend_label,
            "technical_band": tech_band
        }
    }


```

### FILE: src/trace_invest/portfolio/mutate.py
```py
from typing import Dict


def apply_portfolio_action(
    portfolio: Dict,
    action: Dict,
    last_price: float
) -> Dict:

    symbol = action.get("symbol")
    act = action.get("action")
    amount = action.get("amount", 0)

    if act == "BUY":
        shares = amount / last_price

        portfolio["cash"] -= amount

        portfolio["positions"][symbol] = {
            "shares": round(shares, 4),
            "avg_price": round(last_price, 2),
            "value": round(amount, 2)
        }

    elif act == "SELL":
        pos = portfolio["positions"].get(symbol)
        if pos:
            portfolio["cash"] += pos["value"]
            del portfolio["positions"][symbol]

    return portfolio


```

### FILE: src/trace_invest/portfolio/rebalance.py
```py
from typing import Dict, List


TARGET_PCT = 0.05
MAX_PCT = 0.10
MIN_PCT = 0.02


def compute_rebalance_actions(
    portfolio: Dict,
    latest_prices: Dict[str, float],
    decisions: List[Dict]
) -> List[Dict]:

    actions = []

    capital = portfolio["capital"]
    positions = portfolio["positions"]

    decision_map = {
        d["stock"]: d for d in decisions
    }

    for symbol, pos in positions.items():

        price = latest_prices.get(symbol)
        if not price:
            continue

        value = pos["shares"] * price
        pct = value / capital

        # -----------------------
        # TRIM OVERSIZED
        # -----------------------
        if pct > MAX_PCT:
            excess_value = value - capital * TARGET_PCT

            actions.append({
                "action": "TRIM",
                "symbol": symbol,
                "amount": round(excess_value)
            })

        # -----------------------
        # TOP UP UNDERSIZED
        # -----------------------
        if pct < MIN_PCT:
            d = decision_map.get(symbol)
            if not d:
                continue

            entry = d.get("entry_filter", {})
            if entry.get("entry_allowed"):
                needed = capital * TARGET_PCT - value

                actions.append({
                    "action": "ADD",
                    "symbol": symbol,
                    "amount": round(needed)
                })

    return actions


```

### FILE: src/trace_invest/portfolio/store.py
```py
import json
from pathlib import Path

PORTFOLIO_PATH = Path("data/portfolio.json")


def load_portfolio():
    if not PORTFOLIO_PATH.exists():
        return {
            "capital": 0,
            "cash": 0,
            "positions": {}
        }
    return json.loads(PORTFOLIO_PATH.read_text())


def save_portfolio(portfolio):
    PORTFOLIO_PATH.write_text(
        json.dumps(portfolio, indent=2)
    )


```

### FILE: src/trace_invest/portfolio/valuation.py
```py
from typing import Dict


def compute_portfolio_valuation(
    portfolio: Dict,
    latest_prices: Dict[str, float]
) -> Dict:

    invested = 0
    unrealized_pnl = 0

    for symbol, pos in portfolio["positions"].items():
        price = latest_prices.get(symbol)
        if not price:
            continue

        current_value = pos["shares"] * price
        invested += current_value

        cost = pos["shares"] * pos["avg_price"]
        unrealized_pnl += current_value - cost

    total_equity = portfolio["cash"] + invested

    if portfolio["capital"] > 0:
        return_pct = round(
            (total_equity - portfolio["capital"])
            / portfolio["capital"] * 100,
            2
        )
    else:
        return_pct = None

    return {
        "capital": portfolio["capital"],
        "cash": round(portfolio["cash"], 2),
        "invested": round(invested, 2),
        "total_equity": round(total_equity, 2),
        "unrealized_pnl": round(unrealized_pnl, 2),
        "return_pct": return_pct
    }


```

### FILE: src/trace_invest/processing/fundamentals.py
```py
from typing import Dict


def compute_quality_metrics(raw: Dict) -> Dict:
    info = raw.get("info", {})

    return {
        "roe": info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0,
        "debt_to_equity": info.get("debtToEquity", 0) / 100 if info.get("debtToEquity") else 0,
        "operating_margin": info.get("operatingMargins", 0) * 100 if info.get("operatingMargins") else 0,
        "revenue_growth_5y": info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else 0,
    }


def compute_valuation_metrics(raw: Dict) -> Dict:
    info = raw.get("info", {})

    return {
        "pe_ratio": info.get("trailingPE"),
        "pb_ratio": info.get("priceToBook"),
        "fcf_yield": (
            (info.get("freeCashflow") / info.get("marketCap") * 100)
            if info.get("freeCashflow") and info.get("marketCap")
            else 0
        ),
    }


def build_processed_fundamentals(raw: Dict) -> Dict:
    return {
        "quality_metrics": compute_quality_metrics(raw),
        "valuation_metrics": compute_valuation_metrics(raw),
        "financials": raw.get("financials", []),
        "balance_sheet": raw.get("balance_sheet", []),
        "cashflow": raw.get("cashflow", []),
        "governance": {},    # extend later
    }


```

### FILE: src/trace_invest/quality/confidence.py
```py
def confidence_band(coverage: dict, freshness: dict) -> str:
    if coverage["coverage_ratio"] >= 0.75 and freshness["freshness"] == "GOOD":
        return "HIGH"
    if coverage["coverage_ratio"] >= 0.5:
        return "MEDIUM"
    return "LOW"


```

### FILE: src/trace_invest/quality/coverage.py
```py
from typing import Dict

EXPECTED_YEARS = 6


def coverage_score(processed: Dict) -> Dict:
    years = set()

    financials = processed.get("financials", [])

    if isinstance(financials, list):
        for row in financials:
            if isinstance(row, dict):
                for k in row.keys():
                    if k != "index":
                        years.add(k)

    years = sorted(years, reverse=True)
    available = len(years)

    return {
        "available_years": available,
        "expected_years": EXPECTED_YEARS,
        "coverage_ratio": round(available / EXPECTED_YEARS, 2)
        if EXPECTED_YEARS else 0,
        "years": years,
    }

```

### FILE: src/trace_invest/quality/freshness.py
```py
from datetime import datetime, timezone

def freshness_score(years: list[str]) -> dict:
    if not years:
        return {
            "age_days": None,
            "freshness": "UNKNOWN",
        }

    parsed_years = []

    for y in years:
        try:
            # Handles "2025-03-31 00:00:00"
            dt = datetime.fromisoformat(str(y))
            parsed_years.append(dt.year)
        except Exception:
            try:
                # Handles "2025"
                parsed_years.append(int(y))
            except Exception:
                continue

    if not parsed_years:
        return {
            "age_days": None,
            "freshness": "UNKNOWN",
        }

    latest_year = max(parsed_years)
    latest_date = datetime(latest_year, 3, 31, tzinfo=timezone.utc)

    age_days = (datetime.now(timezone.utc) - latest_date).days

    if age_days <= 180:
        label = "GOOD"
    elif age_days <= 365:
        label = "STALE"
    else:
        label = "OLD"

    return {
        "latest_year": latest_year,
        "age_days": age_days,
        "freshness": label,
    }

```

### FILE: src/trace_invest/quality/raw_field_inventory.py
```py
from typing import Dict


def build_raw_field_inventory(raw: Dict) -> Dict:
    """
    Collects all field/column names inside each raw block.
    Used to discover unused potential signals.
    """

    inventory = {}

    for section, block in raw.items():
        fields = {}

        if isinstance(block, dict):
            for k, v in block.items():
                fields[k] = type(v).__name__

        elif isinstance(block, list):
            if block and isinstance(block[0], dict):
                for k, v in block[0].items():
                    fields[k] = type(v).__name__

        inventory[section] = fields

    return inventory


```

### FILE: src/trace_invest/quality/raw_profiler.py
```py
from typing import Dict


def profile_raw_fundamentals(raw: Dict) -> Dict:
    """
    High-level visibility of what blocks exist in raw fundamentals.
    """

    profile = {}

    profile["top_level_keys"] = list(raw.keys())

    info = raw.get("info", {})
    if isinstance(info, dict):
        profile["info_keys"] = list(info.keys())
    else:
        profile["info_keys"] = []

    profile["has_governance_block"] = "governance" in raw

    return profile


```

### FILE: src/trace_invest/quality/raw_schema.py
```py
from typing import Dict


def inspect_raw_schema(raw: Dict) -> Dict:
    """
    Structural view of raw fundamentals.
    Shows type and immediate keys for each section.
    """

    schema = {
        "top_level_keys": list(raw.keys()),
        "sections": {}
    }

    for key, value in raw.items():
        section_info = {
            "type": type(value).__name__
        }

        if isinstance(value, dict):
            section_info["keys"] = list(value.keys())

        elif isinstance(value, list):
            section_info["length"] = len(value)
            if value and isinstance(value[0], dict):
                section_info["sample_keys"] = list(value[0].keys())

        schema["sections"][key] = section_info

    return schema


```

### FILE: src/trace_invest/run_weekly.py
```py
from pathlib import Path
import json
import time
from datetime import datetime, timezone
import csv

from trace_invest.utils.logger import setup_logger
from trace_invest.ingestion.prices import run_weekly_price_ingestion
from trace_invest.validation.runner import run_validation
from trace_invest.intelligence.conviction import conviction_score
from trace_invest.outputs.signals import generate_signal
from trace_invest.outputs.journal import create_journal_entry
from trace_invest.config.loader import load_config
from trace_invest.ingestion.fundamentals import (fetch_fundamentals,write_raw_fundamentals,)
from trace_invest.validation.system_awareness import build_system_awareness
from trace_invest.processing.fundamentals import build_processed_fundamentals
from trace_invest.quality.coverage import coverage_score
from trace_invest.quality.freshness import freshness_score
from trace_invest.quality.confidence import confidence_band
from trace_invest.quality.raw_profiler import profile_raw_fundamentals
from trace_invest.quality.raw_schema import inspect_raw_schema
from trace_invest.quality.raw_field_inventory import build_raw_field_inventory
from trace_invest.outputs.rankings import generate_rankings
from trace_invest.outputs.watchlist import generate_long_term_watchlist
from trace_invest.outputs.narrative import generate_narrative
from trace_invest.outputs.sectors import generate_sector_summary
from trace_invest.outputs.history import update_stock_history
from trace_invest.outputs.trends import compute_trend
from trace_invest.outputs.sector_trends import generate_sector_trends
from trace_invest.technical.trend import compute_price_trend
from trace_invest.technical.momentum import compute_momentum
from trace_invest.technical.score import compute_technical_score
from trace_invest.technical.entry_filter import passes_entry_filter
from trace_invest.portfolio.engine import evaluate_portfolio_action
from trace_invest.portfolio.store import load_portfolio, save_portfolio
from trace_invest.portfolio.mutate import apply_portfolio_action
from trace_invest.portfolio.valuation import compute_portfolio_valuation
from trace_invest.portfolio.rebalance import compute_rebalance_actions
from trace_invest.portfolio.exit_manager import evaluate_exit_override





# -----------------------------------------------------------
# Setup
# -----------------------------------------------------------

logger = setup_logger()

SNAPSHOT_DIR = Path("data/snapshots")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------
# Helpers
# -----------------------------------------------------------

def write_processed_fundamentals(snapshot_dir: Path, symbol: str, processed: dict):
    path = snapshot_dir / "fundamentals.json"

    if path.exists():
        try:
            data = json.loads(path.read_text())
        except Exception:
            data = {}
    else:
        data = {}

    data[symbol] = processed
    path.write_text(json.dumps(data, indent=2))



def build_validation_financials(processed: dict) -> dict:
    summary = {}

    cashflow = processed.get("cashflow") or []
    if cashflow:
        latest = cashflow[0]
        summary["cash_flow_from_ops"] = next(
            (
                v
                for k, v in latest.items()
                if "Operating Cash Flow" in k
                or "Total Cash From Operating Activities" in k
            ),
            0,
        )

    financials = processed.get("financials") or []
    if financials:
        latest = financials[0]
        summary["net_profit"] = next(
            (
                v
                for k, v in latest.items()
                if "Net Income" in k
                or "Net Profit" in k
            ),
            0,
        )

    return summary


def generate_market_summary(decisions: list) -> dict:
    summary = {
        "total_stocks": len(decisions),
        "by_decision_zone": {},
        "by_overall_risk": {},
    }

    for d in decisions:
        zone = d.get("decision_zone")
        risk = d.get("overall_risk")

        summary["by_decision_zone"][zone] = (
            summary["by_decision_zone"].get(zone, 0) + 1
        )

        summary["by_overall_risk"][risk] = (
            summary["by_overall_risk"].get(risk, 0) + 1
        )

    return summary




def load_prices(symbol: str):
    path = Path(f"data/raw/prices/{symbol}.csv")

    if not path.exists():
        return []

    rows = []

    try:
        with path.open() as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append({
                    "date": r.get("date") or r.get("Date"),
                    "close": float(r.get("close") or r.get("Close") or 0),
                })
    except Exception:
        return []

    return rows



# -----------------------------------------------------------
# Main Pipeline
# -----------------------------------------------------------

def run_weekly_pipeline():

    logger.info("===== Weekly TRACE MARKETS run started =====")

    portfolio = load_portfolio()


    # -------------------------------------------------------
    # Snapshot setup
    # -------------------------------------------------------

    run_date = datetime.now(timezone.utc).date().isoformat()
    snapshot_dir = SNAPSHOT_DIR / run_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    snapshot_file = snapshot_dir / "snapshot.json"
    market_summary_file = snapshot_dir / "market_summary.json"

    snapshot = {
        "run_date": run_date,
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "decisions": [],
    }

    # -------------------------------------------------------
    # Load config + universe
    # -------------------------------------------------------

    config = load_config()
    stocks = config["universe"]["universe"]["stocks"]

    # stocks = json.loads(Path(config["universe"]["universe"]["stocks_file"]).read_text())

    logger.info(f"Universe size: {len(stocks)}")

    

    # -------------------------------------------------------
    # Weekly price ingestion
    # -------------------------------------------------------

    run_weekly_price_ingestion()

    # -------------------------------------------------------
    # Per-stock processing
    # -------------------------------------------------------

    latest_prices = {}

    for stock in stocks:
        name = stock["name"]
        symbol = stock["symbol"]

        try:
            logger.info(f"Processing {symbol}")

            # Raw fundamentals
            raw_fundamentals = fetch_fundamentals(symbol)
            write_raw_fundamentals(symbol, raw_fundamentals)

            # Processed fundamentals
            processed = build_processed_fundamentals(raw_fundamentals)

            processed["raw_profile"] = profile_raw_fundamentals(raw_fundamentals)
            processed["raw_schema"] = inspect_raw_schema(raw_fundamentals)
            processed["raw_field_inventory"] = build_raw_field_inventory(
                raw_fundamentals
            )

            # Quality layer
            coverage = coverage_score(processed)
            freshness = freshness_score(coverage.get("years", []))
            confidence = confidence_band(coverage, freshness)

            processed["quality"] = {
                "coverage": coverage,
                "freshness": freshness,
                "confidence": confidence,
            }

            write_processed_fundamentals(snapshot_dir, symbol, processed)

            # Validation
            validation = run_validation(processed)

            # Intelligence
            conviction = conviction_score(processed, validation)
            signal = generate_signal(conviction)

            journal = create_journal_entry(name, signal)
            journal["validation"] = validation
            journal["data_confidence_score"] = validation.get("data_confidence_score")
            journal["data_confidence_band"] = validation.get("data_confidence_band")
                journal["system_awareness"] = build_system_awareness(journal, validation)
            journal["quality"] = {
                "coverage_score": coverage.get("coverage_ratio"),
                "freshness": freshness.get("freshness"),
                "confidence_band": confidence,
            }
            journal["governance"] = validation.get("governance")
            journal["stability"] = validation.get("stability")
            journal["master"] = validation.get("master")
            journal["valuation"] = {
                "valuation_sanity": validation.get("details", {}).get("valuation_sanity", {}).get("status")
                if isinstance(validation.get("details", {}).get("valuation_sanity"), dict)
                else validation.get("details", {}).get("valuation_sanity")
            }
            journal["narrative"] = generate_narrative(journal)

            prices = load_prices(symbol)

            if prices:
                latest_prices[symbol] = prices[-1]["close"]


            technical = compute_price_trend(prices)
            momentum = compute_momentum(prices)
            tech_score = compute_technical_score(technical, momentum)

            journal["technical"] = technical
            journal["momentum"] = momentum
            journal["technical_score"] = tech_score

            entry = passes_entry_filter(journal)
            journal["entry_filter"] = entry

            exit_override = evaluate_exit_override(journal)
            journal["exit_override"] = exit_override
            if journal.get("exit_override", {}).get("exit_override"):
                portfolio_action = {
                    "action": "SELL",
                    "symbol": journal["stock"]
                }
            else:
                portfolio_action = evaluate_portfolio_action(
                    portfolio,
                    journal
                )

            price = prices[-1]["close"] if prices else None

            if price:
                portfolio = apply_portfolio_action(
                    portfolio,
                    portfolio_action,
                    price
                )


            trend = compute_trend(symbol)
            journal["trend"] = trend

            update_stock_history(journal, run_date)

            snapshot["decisions"].append(journal)

            time.sleep(1)


        except Exception:
            logger.exception(f"FAILED processing {symbol}")
            continue
    

    portfolio_summary = compute_portfolio_valuation(
    portfolio,
    latest_prices
    )

    (Path("data/portfolio_summary.json")
    .write_text(json.dumps(portfolio_summary, indent=2)))

    save_portfolio(portfolio)


    rebalance_actions = compute_rebalance_actions(
    portfolio,
    latest_prices,
    snapshot["decisions"]
    )

    (Path("data/rebalance_actions.json")
    .write_text(json.dumps(rebalance_actions, indent=2)))


    # -------------------------------------------------------
    # Rankings
    # -------------------------------------------------------

    rankings = generate_rankings(snapshot["decisions"])
    rankings_path = snapshot_dir / "rankings.json"
    rankings_path.write_text(json.dumps(rankings, indent=2))

    # -------------------------------------------------------
    # Sector Trends
    # -------------------------------------------------------

    sector_trends = generate_sector_trends(
        snapshot["decisions"],
        stocks
    )

    (snapshot_dir / "sector_trends.json").write_text(
        json.dumps(sector_trends, indent=2)
    )



    # -------------------------------------------------------
    # Sector Summary
    # -------------------------------------------------------

    sector_summary = generate_sector_summary(
        snapshot["decisions"],
        stocks
    )

    (snapshot_dir / "sectors.json").write_text(
        json.dumps(sector_summary, indent=2)
    )



    # -------------------------------------------------------
    # Watchlist
    # -------------------------------------------------------

    watchlist = generate_long_term_watchlist(snapshot["decisions"])

    print(watchlist)

    watchlist_dir = Path("data/watchlists")
    watchlist_dir.mkdir(parents=True, exist_ok=True)

    watchlist_path = watchlist_dir / "long_term.json"
    watchlist_path.write_text(json.dumps(watchlist, indent=2))


    # -------------------------------------------------------
    # Market Summary
    # -------------------------------------------------------

    market_summary = generate_market_summary(snapshot["decisions"])
    market_summary_file.write_text(json.dumps(market_summary, indent=2))

    # -------------------------------------------------------
    # Write snapshot
    # -------------------------------------------------------

    snapshot_file.write_text(json.dumps(snapshot, indent=2))

    logger.info(f"Weekly snapshot written: {snapshot_file}")
    logger.info(f"Market summary written: {market_summary_file}")
    logger.info("===== Weekly TRACE MARKETS run completed =====")


# -----------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------

if __name__ == "__main__":
    run_weekly_pipeline()
    run_weekly_pipeline()

```

### FILE: src/trace_invest/stability/consistency.py
```py
from typing import Dict, List
import statistics


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name or keyword.replace("_", " ") in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def _std(values):
    if len(values) < 3:
        return None
    return statistics.pstdev(values)


def analyze_consistency(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    roe_series = _extract_series(financials, "return on equity")
    margin_series = _extract_series(financials, "operating margin")

    roe_vals = []
    margin_vals = []

    for v in roe_series.values():
        try:
            roe_vals.append(float(v))
        except Exception:
            pass

    for v in margin_series.values():
        try:
            margin_vals.append(float(v))
        except Exception:
            pass

    if len(roe_vals) < 3 and len(margin_vals) < 3:
        return {
            "name": "consistency",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Not enough data for consistency analysis",
        }

    roe_std = _std(roe_vals) if len(roe_vals) >= 3 else None
    margin_std = _std(margin_vals) if len(margin_vals) >= 3 else None

    bad = 0

    if roe_std and roe_std > 0.05:
        bad += 1

    if margin_std and margin_std > 0.05:
        bad += 1

    if bad == 0:
        return {
            "name": "consistency",
            "status": "CONSISTENT",
            "risk": "LOW",
            "explanation": "ROE and margins stable across years",
        }

    if bad == 1:
        return {
            "name": "consistency",
            "status": "MODERATE",
            "risk": "MEDIUM",
            "explanation": "One profitability metric shows volatility",
        }

    return {
        "name": "consistency",
        "status": "VOLATILE",
        "risk": "HIGH",
        "explanation": "ROE and margins highly volatile",
        }


```

### FILE: src/trace_invest/stability/fcf_cagr.py
```py
from typing import Dict, List
import math


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name or keyword.replace("_", " ") in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def analyze_fcf_cagr(processed: Dict) -> Dict:
    cashflows = processed.get("cashflow") or []

    series = _extract_series(cashflows, "free cash flow")

    if not series:
        return {
            "name": "fcf_cagr",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Free cash flow history unavailable",
        }

    items = sorted(series.items())
    start_year, start_val = items[0]
    end_year, end_val = items[-1]

    try:
        start = float(start_val)
        end = float(end_val)
    except Exception:
        return {
            "name": "fcf_cagr",
            "status": "ERROR",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Invalid FCF values",
        }

    if start <= 0 or end <= 0:
        return {
            "name": "fcf_cagr",
            "status": "INVALID",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Non-positive FCF values",
        }

    years = max(len(items) - 1, 1)
    cagr = round((end / start) ** (1 / years) - 1, 3)

    if cagr >= 0.12:
        status = "STRONG"
        risk = "LOW"
    elif cagr >= 0.05:
        status = "MODERATE"
        risk = "LOW"
    elif cagr >= 0:
        status = "WEAK"
        risk = "MEDIUM"
    else:
        status = "DECLINING"
        risk = "HIGH"

    return {
        "name": "fcf_cagr",
        "status": status,
        "risk": risk,
        "value": cagr,
        "explanation": "Free cash flow compound annual growth rate",
    }


```

### FILE: src/trace_invest/stability/median_operating_margin.py
```py
from typing import Dict, List
import statistics


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name or keyword.replace("_", " ") in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def analyze_median_operating_margin(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    series = _extract_series(financials, "operating margin")

    if not series:
        return {
            "name": "median_operating_margin",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Operating margin history unavailable",
        }

    values = []

    for v in series.values():
        try:
            values.append(float(v))
        except Exception:
            continue

    if len(values) < 3:
        return {
            "name": "median_operating_margin",
            "status": "INSUFFICIENT",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Less than 3 years of operating margin data",
        }

    median_margin = round(statistics.median(values), 2)

    if median_margin >= 0.25:
        status = "EXCELLENT"
        risk = "LOW"
    elif median_margin >= 0.15:
        status = "GOOD"
        risk = "LOW"
    elif median_margin >= 0.08:
        status = "AVERAGE"
        risk = "MEDIUM"
    else:
        status = "WEAK"
        risk = "HIGH"

    return {
        "name": "median_operating_margin",
        "status": status,
        "risk": risk,
        "value": median_margin,
        "explanation": "5-year median operating margin",
    }


```

### FILE: src/trace_invest/stability/median_roe.py
```py
from typing import Dict, List
import statistics


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name or keyword.replace("_", " ") in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def analyze_median_roe(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    series = _extract_series(financials, "return on equity")


    if not series:
        return {
            "name": "median_roe",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "ROE history unavailable",
        }

    values = []

    for v in series.values():
        try:
            values.append(float(v))
        except Exception:
            continue

    if len(values) < 3:
        return {
            "name": "median_roe",
            "status": "INSUFFICIENT",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Less than 3 years of ROE data",
        }

    median_roe = round(statistics.median(values), 2)

    if median_roe >= 0.18:
        status = "EXCELLENT"
        risk = "LOW"
    elif median_roe >= 0.12:
        status = "GOOD"
        risk = "LOW"
    elif median_roe >= 0.08:
        status = "AVERAGE"
        risk = "MEDIUM"
    else:
        status = "WEAK"
        risk = "HIGH"

    return {
        "name": "median_roe",
        "status": status,
        "risk": risk,
        "value": median_roe,
        "explanation": "5-year median return on equity",
    }


```

### FILE: src/trace_invest/stability/registry.py
```py
from trace_invest.stability.median_roe import analyze_median_roe
from trace_invest.stability.median_operating_margin import analyze_median_operating_margin
from trace_invest.stability.revenue_cagr import analyze_revenue_cagr
from trace_invest.stability.fcf_cagr import analyze_fcf_cagr
from trace_invest.stability.consistency import analyze_consistency
from trace_invest.stability.stability_taxonomy import analyze_stability_taxonomy


STABILITY_ENGINES = [
    analyze_median_roe,
    analyze_median_operating_margin,
    analyze_revenue_cagr,
    analyze_fcf_cagr,
    analyze_consistency,
    analyze_stability_taxonomy,
]


```

### FILE: src/trace_invest/stability/revenue_cagr.py
```py
from typing import Dict, List
import math


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name or keyword.replace("_", " ") in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def analyze_revenue_cagr(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    series = _extract_series(financials, "revenue")

    if not series:
        return {
            "name": "revenue_cagr",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Revenue history unavailable",
        }

    items = sorted(series.items())
    start_year, start_val = items[0]
    end_year, end_val = items[-1]

    try:
        start = float(start_val)
        end = float(end_val)
    except Exception:
        return {
            "name": "revenue_cagr",
            "status": "ERROR",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Invalid revenue values",
        }

    if start <= 0 or end <= 0:
        return {
            "name": "revenue_cagr",
            "status": "INVALID",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Non-positive revenue values",
        }

    years = max(len(items) - 1, 1)
    cagr = round((end / start) ** (1 / years) - 1, 3)

    if cagr >= 0.12:
        status = "STRONG"
        risk = "LOW"
    elif cagr >= 0.05:
        status = "MODERATE"
        risk = "LOW"
    elif cagr >= 0:
        status = "WEAK"
        risk = "MEDIUM"
    else:
        status = "DECLINING"
        risk = "HIGH"

    return {
        "name": "revenue_cagr",
        "status": status,
        "risk": risk,
        "value": cagr,
        "explanation": "Revenue compound annual growth rate",
    }


```

### FILE: src/trace_invest/stability/stability_score.py
```py
from typing import Dict

RISK_POINTS = {
    "LOW": 0,
    "MEDIUM": 2,
    "HIGH": 5,
    "UNKNOWN": 1,
}


def compute_stability_score(details: Dict) -> Dict:
    total = 0
    max_total = 0
    weak = []

    taxonomy = details.get("stability_taxonomy", {})
    taxonomy_status = taxonomy.get("status")

    for name, result in details.items():
        if not name.startswith(("median_", "revenue_cagr", "fcf_cagr", "consistency")):
            continue

        risk = result.get("risk", "UNKNOWN")
        points = RISK_POINTS.get(risk, 1)

        total += points
        max_total += 5

        if risk in ("HIGH", "MEDIUM"):
            weak.append(f"{name}:{result.get('status')}")

    if max_total == 0:
        score = 100
    else:
        score = round(100 - (total / max_total) * 100)

    # Taxonomy override: only structural decline should force WEAK.
    if taxonomy_status == "STRUCTURAL_DECLINE":
        weak.append("stability_taxonomy:STRUCTURAL_DECLINE")
        score = min(score, 49)
    elif taxonomy_status in ("STABLE_LOW_GROWTH", "CYCLICAL"):
        score = max(score, 50)

    if score >= 75:
        band = "STRONG"
    elif score >= 50:
        band = "AVERAGE"
    else:
        band = "WEAK"

    return {
        "stability_score": score,
        "stability_band": band,
        "weak_areas": weak,
    }


```

### FILE: src/trace_invest/stability/stability_taxonomy.py
```py
from typing import Dict, List, Optional

from trace_invest.stability.revenue_cagr import analyze_revenue_cagr
from trace_invest.stability.fcf_cagr import analyze_fcf_cagr
from trace_invest.stability.consistency import analyze_consistency
from trace_invest.stability.median_operating_margin import analyze_median_operating_margin
from trace_invest.governance.balance_sheet_stress import analyze_balance_sheet_stress

LOW_GROWTH_MAX = 0.05
MEAN_REVERTING_MAX = 0.03
POSITIVE_FCF_YEARS_REQUIRED = 2


def analyze_stability_taxonomy(processed: Dict) -> Dict:
    revenue = analyze_revenue_cagr(processed)
    fcf = analyze_fcf_cagr(processed)
    consistency = analyze_consistency(processed)
    margin = analyze_median_operating_margin(processed)
    leverage = analyze_balance_sheet_stress(processed)

    if _has_missing(revenue, fcf, consistency, margin, leverage):
        return {
            "name": "stability_taxonomy",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Insufficient data to classify stability taxonomy",
        }

    revenue_cagr = revenue.get("value")
    fcf_cagr = fcf.get("value")
    margin_status = margin.get("status")
    leverage_status = leverage.get("status")

    strong_cashflows = _has_strong_cashflows(processed)
    no_leverage_stress = leverage_status in ("STABLE", "MANAGED")

    if _is_structural_decline(revenue_cagr, fcf_cagr, margin_status):
        return {
            "name": "stability_taxonomy",
            "status": "STRUCTURAL_DECLINE",
            "risk": "HIGH",
            "explanation": "Negative growth with margin erosion",
        }

    if _is_stable_low_growth(revenue_cagr, fcf_cagr, strong_cashflows, no_leverage_stress):
        return {
            "name": "stability_taxonomy",
            "status": "STABLE_LOW_GROWTH",
            "risk": "MEDIUM",
            "explanation": "Low growth with resilient cash flows and limited leverage stress",
        }

    if _is_cyclical(revenue_cagr, fcf_cagr, consistency.get("status")):
        return {
            "name": "stability_taxonomy",
            "status": "CYCLICAL",
            "risk": "MEDIUM",
            "explanation": "Volatile results with mean-reverting growth",
        }

    return {
        "name": "stability_taxonomy",
        "status": "STABLE_LOW_GROWTH",
        "risk": "MEDIUM",
        "explanation": "No structural decline detected",
    }


def _has_missing(*items: Dict) -> bool:
    for item in items:
        status = item.get("status")
        risk = item.get("risk")
        if status in ("NO_DATA", "UNKNOWN", "ERROR", "INVALID", "INSUFFICIENT"):
            return True
        if risk == "UNKNOWN":
            return True
    return False


def _is_structural_decline(
    revenue_cagr: Optional[float],
    fcf_cagr: Optional[float],
    margin_status: Optional[str],
) -> bool:
    if revenue_cagr is None or fcf_cagr is None:
        return False
    return revenue_cagr < 0 and fcf_cagr < 0 and margin_status == "WEAK"


def _is_stable_low_growth(
    revenue_cagr: Optional[float],
    fcf_cagr: Optional[float],
    strong_cashflows: bool,
    no_leverage_stress: bool,
) -> bool:
    if revenue_cagr is None or fcf_cagr is None:
        return False

    low_growth = revenue_cagr <= LOW_GROWTH_MAX and revenue_cagr >= 0
    fcf_positive = fcf_cagr >= 0

    return low_growth and fcf_positive and strong_cashflows and no_leverage_stress


def _is_cyclical(
    revenue_cagr: Optional[float],
    fcf_cagr: Optional[float],
    consistency_status: Optional[str],
) -> bool:
    if revenue_cagr is None or fcf_cagr is None:
        return False

    mean_reverting = abs(revenue_cagr) <= MEAN_REVERTING_MAX and abs(fcf_cagr) <= MEAN_REVERTING_MAX
    volatile = consistency_status in ("VOLATILE", "MODERATE")

    return mean_reverting and volatile


def _has_strong_cashflows(processed: Dict) -> bool:
    cashflows = processed.get("cashflow") or []
    series = _extract_series(cashflows, "free cash flow")

    if not series:
        return False

    years = sorted(series.keys(), reverse=True)
    positive_years = 0

    for year in years[:3]:
        try:
            value = float(series.get(year, 0))
        except Exception:
            continue
        if value > 0:
            positive_years += 1

    return positive_years >= POSITIVE_FCF_YEARS_REQUIRED


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name or keyword.replace("_", " ") in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}

```

### FILE: src/trace_invest/technical/entry_filter.py
```py
from typing import Dict


def passes_entry_filter(decision: Dict) -> Dict:

    v = decision.get("validation", {})
    master = v.get("master", {})
    governance = v.get("governance", {})
    tech = decision.get("technical_score", {})

    master_band = master.get("master_band")
    gov_band = governance.get("governance_band")
    tech_band = tech.get("technical_band")

    allowed = (
        master_band in ("GOOD", "ELITE")
        and gov_band == "LOW"
        and tech_band == "STRONG"
    )

    return {
        "entry_allowed": allowed,
        "reason": {
            "master_band": master_band,
            "governance_band": gov_band,
            "technical_band": tech_band,
        }
    }


```

### FILE: src/trace_invest/technical/momentum.py
```py
from typing import List, Dict


def compute_momentum(prices: List[Dict]) -> Dict:
    """
    prices: list of {date, close}
    Assumes chronological order
    """

    if not prices or len(prices) < 252:
        return {
            "return_6m": None,
            "return_12m": None,
            "momentum": "NO_DATA",
        }

    closes = [p["close"] for p in prices]

    last = closes[-1]
    m6 = closes[-126]   # approx 6 months
    m12 = closes[-252] # approx 12 months

    r6 = round((last - m6) / m6 * 100, 1)
    r12 = round((last - m12) / m12 * 100, 1)

    if r6 > 0 and r12 > 0:
        label = "POSITIVE"
    elif r6 < 0 and r12 < 0:
        label = "NEGATIVE"
    else:
        label = "MIXED"

    return {
        "return_6m": r6,
        "return_12m": r12,
        "momentum": label,
    }


```

### FILE: src/trace_invest/technical/score.py
```py
from typing import Dict


def compute_technical_score(technical: Dict, momentum: Dict) -> Dict:

    score = 0

    trend = technical.get("trend")
    mom = momentum.get("momentum")

    # Trend contribution
    if trend == "UP":
        score += 50
    elif trend == "SIDEWAYS":
        score += 25

    # Momentum contribution
    if mom == "POSITIVE":
        score += 50
    elif mom == "MIXED":
        score += 25

    if score >= 70:
        band = "STRONG"
    elif score >= 40:
        band = "NEUTRAL"
    else:
        band = "WEAK"

    return {
        "technical_score": score,
        "technical_band": band,
    }


```

### FILE: src/trace_invest/technical/trend.py
```py
from typing import List, Dict


def compute_price_trend(prices: List[Dict]) -> Dict:
    """
    prices: list of {date, close}
    """

    if not prices or len(prices) < 200:
        return {
            "trend": "NO_DATA",
            "ma50": None,
            "ma200": None,
        }

    closes = [p["close"] for p in prices]

    ma50 = sum(closes[-50:]) / 50
    ma200 = sum(closes[-200:]) / 200
    last_price = closes[-1]

    if last_price > ma50 > ma200:
        trend = "UP"
    elif last_price < ma50 < ma200:
        trend = "DOWN"
    else:
        trend = "SIDEWAYS"

    return {
        "trend": trend,
        "ma50": round(ma50, 2),
        "ma200": round(ma200, 2),
    }


```

### FILE: src/trace_invest/utils/__init__.py
```py

```

### FILE: src/trace_invest/utils/logger.py
```py
from loguru import logger
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(
    level: str = "INFO",
    log_file: str = "trace-invest.log",
):
    logger.remove()

    # Console logging
    logger.add(
        sys.stdout,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
    )

    # File logging
    logger.add(
        LOG_DIR / log_file,
        level=level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    )

    logger.info("Logger initialized")
    return logger

```

### FILE: src/trace_invest/validation/__init__.py
```py

```

### FILE: src/trace_invest/validation/data_confidence.py
```py
from typing import Dict

DATA_CONFIDENCE_START = 100
DATA_CONFIDENCE_PENALTY = 12
DATA_CONFIDENCE_MIN = 0
DATA_CONFIDENCE_MAX = 100

GOVERNANCE_METRICS = {
    "earnings_quality",
    "unusual_items",
    "tax_volatility",
    "capital_allocation",
    "balance_sheet_stress",
}

STABILITY_METRICS = {
    "median_roe",
    "median_operating_margin",
    "revenue_cagr",
    "fcf_cagr",
    "consistency",
    "stability_taxonomy",
}


def compute_data_confidence(details: Dict) -> Dict:
    score = DATA_CONFIDENCE_START
    missing = 0

    for name, detail in details.items():
        if name not in GOVERNANCE_METRICS and name not in STABILITY_METRICS:
            continue

        status = detail.get("status")
        risk = detail.get("risk") or detail.get("risk_level")

        if status in ("NO_DATA", "UNKNOWN") or risk == "UNKNOWN":
            missing += 1
            score -= DATA_CONFIDENCE_PENALTY

    score = max(DATA_CONFIDENCE_MIN, min(DATA_CONFIDENCE_MAX, score))

    if score >= 75:
        band = "HIGH"
    elif score >= 50:
        band = "MEDIUM"
    else:
        band = "LOW"

    return {
        "data_confidence_score": score,
        "data_confidence_band": band,
        "missing_metric_count": missing,
    }

```

### FILE: src/trace_invest/validation/fraud.py
```py
from typing import Dict, List


def check_basic_fraud_flags(financials: Dict) -> Dict:
    """
    Basic fraud-related red flags.
    Input: normalized financial data (processed layer)
    Output: flags + explanations
    """

    # Defensive: validation must never crash
    if not isinstance(financials, dict):
        return {
            "layer": "fraud",
            "flag_count": 0,
            "flags": [],
            "risk_level": _risk_level(0),
        }

    flags: List[str] = []

    cfo = financials.get("cash_flow_from_ops")
    profit = financials.get("net_profit")
    recv_growth = financials.get("receivables_growth_pct")
    rpt_pct = financials.get("related_party_txn_pct")

    if cfo is not None and profit is not None:
        if cfo < 0 and profit > 0:
            flags.append("Net profit positive but operating cash flow negative")

    if recv_growth is not None:
        if recv_growth > 30:
            flags.append("Receivables growing unusually fast")

    if rpt_pct is not None:
        if rpt_pct > 10:
            flags.append("High related party transactions")

    return {
        "layer": "fraud",
        "flag_count": len(flags),
        "flags": flags,
        "risk_level": _risk_level(len(flags)),
    }


def _risk_level(flag_count: int) -> str:
    if flag_count == 0:
        return "LOW"
    if flag_count <= 2:
        return "MEDIUM"
    return "HIGH"


```

### FILE: src/trace_invest/validation/governance.py
```py
from typing import Dict

from trace_invest.validation.fraud import check_basic_fraud_flags
from trace_invest.validation.registry import GOVERNANCE_ENGINES
from trace_invest.stability.registry import STABILITY_ENGINES
from trace_invest.stability.stability_score import compute_stability_score
from trace_invest.valuation.registry import VALUATION_ENGINES
from trace_invest.intelligence.master_score import compute_master_score


def run_validation(processed: Dict) -> Dict:
    """
    Runs all validation engines.
    """

    fraud_result = check_basic_fraud_flags(
        processed.get("financials", {})
    )

    details = {
        "fraud": fraud_result
    }

    total_flags = fraud_result["flag_count"]

    for engine in GOVERNANCE_ENGINES:
        result = engine(processed)
        details[result["name"]] = result

        if result.get("risk") == "HIGH":
            total_flags += 1

    governance_summary = compute_governance_score(details)


    for engine in STABILITY_ENGINES:
        result = engine(processed)
        details[result["name"]] = result

        if result.get("risk") == "HIGH":
            total_flags += 1
    
    stability_summary = compute_stability_score(details)

  
    for engine in VALUATION_ENGINES:
        result = engine(processed)
        details[result["name"]] = result

        if result.get("risk") == "HIGH":
            total_flags += 1

    master = compute_master_score({
            "governance": governance_summary,
            "stability": stability_summary,
            "details": details,
        })

    return {
        "total_flags": total_flags,
        "overall_risk": _overall_risk(total_flags),
        "details": details,
        "stability": stability_summary,
        "master": master,
    }


def _overall_risk(total_flags: int) -> str:
    if total_flags == 0:
        return "LOW"
    if total_flags <= 3:
        return "MEDIUM"
    return "HIGH"

```

### FILE: src/trace_invest/validation/governance_score.py
```py
from typing import Dict

RISK_POINTS = {
    "LOW": 0,
    "MEDIUM": 2,
    "HIGH": 5,
    "UNKNOWN": 1,
}


def compute_governance_score(details: Dict) -> Dict:
    total = 0
    max_total = 0
    risks = []

    for name, result in details.items():
        if name in ("fraud",):
            continue

        risk = result.get("risk", "UNKNOWN")
        points = RISK_POINTS.get(risk, 1)

        total += points
        max_total += 5

        if risk in ("HIGH", "MEDIUM"):
            risks.append(f"{name}:{result.get('status')}")

    if max_total == 0:
        score = 100
    else:
        score = round(100 - (total / max_total) * 100)

    if score >= 75:
        band = "LOW"
    elif score >= 50:
        band = "MEDIUM"
    else:
        band = "HIGH"

    return {
        "governance_score": score,
        "governance_band": band,
        "top_risks": risks,
    }


```

### FILE: src/trace_invest/validation/registry.py
```py
from trace_invest.governance.earnings_quality import analyze_earnings_quality
from trace_invest.governance.unusual_items import analyze_unusual_items
from trace_invest.governance.tax_volatility import analyze_tax_volatility
from trace_invest.governance.capital_allocation import analyze_capital_allocation
from trace_invest.governance.balance_sheet_stress import analyze_balance_sheet_stress

GOVERNANCE_ENGINES = [
    analyze_earnings_quality,
    analyze_unusual_items,
    analyze_tax_volatility,
    analyze_capital_allocation,
    analyze_balance_sheet_stress,
    ]


```

### FILE: src/trace_invest/validation/runner.py
```py
from typing import Dict

from trace_invest.validation.fraud import check_basic_fraud_flags
from trace_invest.validation.registry import GOVERNANCE_ENGINES
from trace_invest.stability.registry import STABILITY_ENGINES
from trace_invest.stability.stability_score import compute_stability_score
from trace_invest.valuation.registry import VALUATION_ENGINES
from trace_invest.intelligence.master_score import compute_master_score
from trace_invest.validation.governance_score import compute_governance_score
from trace_invest.validation.data_confidence import compute_data_confidence



def run_validation(processed: Dict) -> Dict:
    """
    Runs all validation engines.
    """

    fraud_result = check_basic_fraud_flags(
        processed.get("financials", {})
    )

    details = {
        "fraud": fraud_result
    }

    total_flags = fraud_result["flag_count"]

    for engine in GOVERNANCE_ENGINES:
        result = engine(processed)
        details[result["name"]] = result

        if result.get("risk") == "HIGH":
            total_flags += 1

    governance_summary = compute_governance_score(details)


    for engine in STABILITY_ENGINES:
        result = engine(processed)
        details[result["name"]] = result

        if result.get("risk") == "HIGH":
            total_flags += 1
    
    stability_summary = compute_stability_score(details)

  
    for engine in VALUATION_ENGINES:
        result = engine(processed)
        details[result["name"]] = result

        if result.get("risk") == "HIGH":
            total_flags += 1

    master = compute_master_score({
            "governance": governance_summary,
            "stability": stability_summary,
            "details": details,
        })

    data_confidence = compute_data_confidence(details)

    return {
        "total_flags": total_flags,
        "overall_risk": _overall_risk(total_flags),
        "data_confidence_score": data_confidence.get("data_confidence_score"),
        "data_confidence_band": data_confidence.get("data_confidence_band"),
        "details": details,
        "governance": governance_summary,
        "stability": stability_summary,
        "master": master,
    }


def _overall_risk(total_flags: int) -> str:
    if total_flags == 0:
        return "LOW"
    if total_flags <= 3:
        return "MEDIUM"
    return "HIGH"

```

### FILE: src/trace_invest/validation/system_awareness.py
```py
from typing import Dict, List

MISSING_STATUSES = {
    "NO_DATA",
    "UNKNOWN",
    "INSUFFICIENT",
    "ERROR",
    "INVALID",
}

DECLINING_STATUSES = {
    "DECLINING",
    "STRUCTURAL_DECLINE",
}

HIGH_RISK_STATUSES = {
    "STRESSED",
    "PERSISTENT",
}


def build_system_awareness(decision: Dict, validation: Dict) -> Dict:
    details = validation.get("details", {})

    missing_inputs = _missing_inputs(details)
    weak_signals = _weak_signals(details)

    # Confidence only reflects data completeness, not the verdict itself.
    confidence_level = _confidence_level(len(missing_inputs))
    assessment_quality = _assessment_quality(len(missing_inputs))
    explanation = _explanation(missing_inputs, weak_signals, confidence_level)

    return {
        "confidence_level": confidence_level,
        "missing_inputs": missing_inputs,
        "weak_signals": weak_signals,
        "assessment_quality": assessment_quality,
        "explanation": explanation,
    }


def _missing_inputs(details: Dict) -> List[str]:
    missing = []

    for name, detail in details.items():
        status = detail.get("status")
        risk = detail.get("risk") or detail.get("risk_level")

        if status in MISSING_STATUSES or risk == "UNKNOWN":
            missing.append(name)

    return sorted(set(missing))


def _weak_signals(details: Dict) -> List[str]:
    weak = []

    for name, detail in details.items():
        status = detail.get("status")
        risk = detail.get("risk") or detail.get("risk_level")

        # High-risk or declining signals are surfaced for transparency.
        if risk == "HIGH":
            weak.append(f"{name}:{status}")
            continue

        if status in DECLINING_STATUSES or status in HIGH_RISK_STATUSES:
            weak.append(f"{name}:{status}")

    return sorted(set(weak))


def _confidence_level(missing_count: int) -> str:
    if missing_count >= 3:
        return "LOW"
    if missing_count >= 1:
        return "MEDIUM"
    return "HIGH"


def _assessment_quality(missing_count: int) -> str:
    if missing_count == 0:
        return "FINAL"
    if missing_count <= 2:
        return "PROVISIONAL"
    return "FRAGILE"


def _explanation(missing_inputs: List[str], weak_signals: List[str], confidence_level: str) -> str:
    if not missing_inputs:
        if weak_signals:
            return (
                "All critical data is present, but high-risk signals were detected; "
                "treat the verdict with caution."
            )
        return "All critical data is present; the verdict reflects full coverage."

    missing_summary = ", ".join(missing_inputs[:5])
    if len(missing_inputs) > 5:
        missing_summary += " (and others)"

    return (
        f"Confidence is {confidence_level} because key inputs are missing: {missing_summary}. "
        "Treat the verdict as provisional."
    )

```

### FILE: src/trace_invest/valuation/registry.py
```py
from trace_invest.valuation.sanity import analyze_valuation_sanity

VALUATION_ENGINES = [
    analyze_valuation_sanity,
]


```

### FILE: src/trace_invest/valuation/sanity.py
```py
from typing import Dict


def analyze_valuation_sanity(processed: Dict) -> Dict:
    valuation = processed.get("valuation_metrics") or {}

    pe = valuation.get("pe_ratio")
    pb = valuation.get("pb_ratio")
    fcf_yield = valuation.get("fcf_yield")

    bad = 0

    if pe is not None and pe > 40:
        bad += 1

    if pb is not None and pb > 8:
        bad += 1

    if fcf_yield is not None and fcf_yield < 0.02:
        bad += 1

    if bad == 0:
        return {
            "name": "valuation_sanity",
            "status": "REASONABLE",
            "risk": "LOW",
            "explanation": "Valuation within sane ranges",
        }

    if bad == 1:
        return {
            "name": "valuation_sanity",
            "status": "RICH",
            "risk": "MEDIUM",
            "explanation": "One valuation metric stretched",
        }

    return {
        "name": "valuation_sanity",
        "status": "EXPENSIVE",
        "risk": "HIGH",
        "explanation": "Multiple valuation metrics stretched",
    }


```

### FILE: tools/build_snapshot.py
```py
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from trace_invest.pipeline.snapshot_builder import build_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a deterministic Trace Invest snapshot",
    )
    parser.add_argument(
        "--date",
        help="Snapshot date in YYYY-MM-DD format",
    )

    args = parser.parse_args()
    os.chdir(ROOT)
    build_snapshot(run_date=args.date)


if __name__ == "__main__":
    main()

```

### FILE: tools/md_to_project.py
```py
import os
import re

# ========= CONFIG =========

SOURCE_MD = "TRACE_CODEBASE.md"
OUTPUT_ROOT = "."

# ==========================

FILE_BLOCK_PATTERN = re.compile(
    r"### FILE: (.*?)\n```[a-zA-Z0-9]*\n([\s\S]*?)\n```",
    re.MULTILINE
)

def main():
    if not os.path.exists(SOURCE_MD):
        print(f"ERROR: {SOURCE_MD} not found")
        return

    with open(SOURCE_MD, "r", encoding="utf-8") as f:
        content = f.read()

    matches = FILE_BLOCK_PATTERN.findall(content)

    if not matches:
        print("No file blocks found.")
        return

    written = 0

    for rel_path, body in matches:
        rel_path = rel_path.strip()
        full_path = os.path.join(OUTPUT_ROOT, rel_path)

        folder = os.path.dirname(full_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(body)

        written += 1

    print(f"Rebuilt {written} files from {SOURCE_MD}")

if __name__ == "__main__":
    main()


```

### FILE: tools/project_to_md.py
```py
import os

OUTPUT = "TRACE_CODEBASE.md"

# Exact folders that contain real source code
ALLOWED_PATH_PREFIXES = [
    "backend",
    "configs",
    "docs",
    "tools",
    "scripts",
    "src/trace_invest",
    "frontend/app",
    "frontend/components",
    "frontend/lib",
]

ALLOWED_EXACT_PATHS = {
    "README.md",
    "docker-compose.yml",
    "pyproject.toml",
    "requirements.txt",
    "frontend/package.json",
    "frontend/package-lock.json",
    "frontend/next.config.ts",
    "frontend/next.config.js",
    "frontend/tsconfig.json",
    "frontend/tailwind.config.js",
    "frontend/tailwind.config.mjs",
    "frontend/eslint.config.mjs",
    "backend/Dockerfile",
    "frontend/Dockerfile",
}

# Allowed file types
ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".html",
    ".css",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".sh",
    ".bat"
}

def allowed_path(path):
    path = path.replace("\\", "/")
    return path in ALLOWED_EXACT_PATHS or any(
        path.startswith(prefix) for prefix in ALLOWED_PATH_PREFIXES
    )

def allowed_file(filename):
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

files = []

for root, dirs, filenames in os.walk("."):
    dirs[:] = sorted(
        d for d in dirs if d not in {".git", ".next", "node_modules", "__pycache__"}
    )
    for name in filenames:
        rel = os.path.relpath(os.path.join(root, name), ".")
        rel = rel.replace("\\", "/")

        if allowed_path(rel) and allowed_file(name):
            files.append(rel)

files = sorted(files)

with open(OUTPUT, "w", encoding="utf-8") as out:
    out.write("# TRACE CODEBASE SNAPSHOT\n\n")

    out.write("## PROJECT TREE\n")
    for f in files:
        out.write(f"{f}\n")

    out.write("\n---\n")

    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as src:
                data = src.read()
        except:
            continue

        ext = f.split(".")[-1]
        out.write(f"\n### FILE: {f}\n")
        out.write(f"```{ext}\n")
        out.write(data)
        out.write("\n```\n")

print(f"TRACE_CODEBASE.md generated with {len(files)} source files only")

```

### FILE: tools/system_state_to_md.py
```py
import os
import hashlib
from datetime import datetime, timezone

OUTPUT = "TRACE_SYSTEM_STATE.md"

ALLOWED_PATHS = [
    "configs",
    "data",
    "backend/Dockerfile",
    "frontend/Dockerfile",
    "docker-compose.yml"
]

MAX_HASH_SIZE = 2_000_000  # 2MB

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()[:16]

def file_info(path):
    size = os.path.getsize(path)
    info = f"size={size}B"
    if size <= MAX_HASH_SIZE:
        info += f" sha256={sha256(path)}"
    return info

def allowed(path):
    path = path.replace("\\", "/")
    return any(
        path == p or path.startswith(p + "/")
        for p in ALLOWED_PATHS
    )

with open(OUTPUT, "w", encoding="utf-8") as out:

    out.write("# TRACE SYSTEM STATE\n\n")
    out.write(f"generated_at: {datetime.now(timezone.utc).isoformat()}\n\n")

    for root, dirs, files in os.walk("."):
        dirs[:] = sorted(
            d for d in dirs if d not in {".git", ".next", "node_modules", "__pycache__"}
        )
        files = sorted(files)
        for name in files:
            rel = os.path.relpath(os.path.join(root, name), ".")
            rel = rel.replace("\\", "/")

            if not allowed(rel):
                continue

            try:
                info = file_info(rel)
            except:
                continue

            out.write(f"{rel} | {info}\n")

print("TRACE_SYSTEM_STATE.md generated (clean)")

```
