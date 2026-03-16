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
