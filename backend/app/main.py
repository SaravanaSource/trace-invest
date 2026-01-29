from fastapi import FastAPI

from backend.app.api.market import router as market_router
from backend.app.api.stocks import router as stocks_router
from backend.app.api.snapshots import router as snapshots_router

app = FastAPI(
    title="TRACE MARKETS API",
    version="0.1.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(market_router)
app.include_router(stocks_router)
app.include_router(snapshots_router)
