from fastapi import APIRouter, HTTPException
from app.services.snapshot_loader import load_latest_market_summary

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/summary")
def get_market_summary():
    try:
        return load_latest_market_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
