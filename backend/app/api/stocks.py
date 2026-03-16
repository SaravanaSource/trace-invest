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
