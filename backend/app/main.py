from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.market import router as market_router
from app.api.stocks import router as stocks_router
from app.api.snapshots import router as snapshots_router

app = FastAPI(
    title="TRACE MARKETS API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(market_router)
app.include_router(stocks_router)
app.include_router(snapshots_router)
