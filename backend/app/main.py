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
from backend.app.api.phase2 import router as phase2_router
from trace_invest.api.research import router as research_router
from trace_invest.api.alpha import router as alpha_router
from trace_invest.api.auth import router as auth_router
from trace_invest.api.portfolio import router as portfolio_router
from trace_invest.api.watchlist import router as watchlist_router
from trace_invest.api.alerts import router as alerts_router
from trace_invest.api.health import router as health_router
from trace_invest.api.admin import router as admin_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Trace Markets API")

# CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks_router)
app.include_router(market_router)
app.include_router(snapshots_router)
app.include_router(history_router)
app.include_router(phase2_router)
app.include_router(research_router)
app.include_router(alpha_router)
app.include_router(auth_router)
app.include_router(portfolio_router)
app.include_router(watchlist_router)
app.include_router(alerts_router)
app.include_router(health_router)
app.include_router(admin_router)

# Serve a lightweight static research UI so frontend dev build is optional
STATIC_DIR = BASE_DIR / "app" / "static"
if STATIC_DIR.exists():
    app.mount("/research-ui", StaticFiles(directory=str(STATIC_DIR / "research_ui"), html=True), name="research_ui")
