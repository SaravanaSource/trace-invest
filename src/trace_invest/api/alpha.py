from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/alpha", tags=["alpha"])

DATA_DIR = Path(__file__).resolve().parents[3] / "data"


def _read_optional(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


@router.get("/signals")
def get_signals():
    return _read_optional(DATA_DIR / "signals" / "signals.json")


@router.get("/strategies")
def get_strategies():
    return _read_optional(DATA_DIR / "generated_strategies" / "generated_strategies.json")


@router.get("/rankings")
def get_rankings():
    return _read_optional(DATA_DIR / "strategy_rankings" / "strategy_rankings.json")


@router.get("/monitoring")
def get_monitoring():
    return _read_optional(DATA_DIR / "strategy_monitoring" / "strategy_monitoring.json")


@router.get("/top")
def get_top():
    # return top 5 by alpha score if available
    r = _read_optional(DATA_DIR / "strategy_rankings" / "strategy_rankings.json").get("rankings", [])
    return {"top": r[:5]}
