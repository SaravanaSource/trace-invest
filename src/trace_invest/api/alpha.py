from fastapi import APIRouter, HTTPException
import json
from typing import List

from trace_invest.db import SessionLocal
from trace_invest.db.models import StrategyResult
from trace_invest.config import data_path

router = APIRouter(prefix="/alpha", tags=["alpha"])

# Use canonical data root (trace-invest/src/data) via config.data_path()
DATA_DIR = data_path()


def _read_required_json(path):
    """Return parsed JSON or raise an HTTPException with helpful detail."""
    if not path.exists():
        raise HTTPException(status_code=404, detail={"error": "Data not found. Run pipeline."})
    try:
        return json.loads(path.read_text())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": f"Failed to read JSON: {e}"})


@router.get("/signals")
def get_signals():
    return _read_required_json(DATA_DIR / "signals" / "signals.json")


@router.get("/strategies")
def get_strategies():
    return _read_required_json(DATA_DIR / "generated_strategies" / "generated_strategies.json")


@router.get("/rankings")
def get_rankings():
    return _read_required_json(DATA_DIR / "strategy_rankings" / "strategy_rankings.json")


@router.get("/monitoring")
def get_monitoring():
    return _read_required_json(DATA_DIR / "strategy_monitoring" / "strategy_monitoring.json")


@router.get("/top")
def get_top():
    # return top 5 by alpha score if available
    r = _read_required_json(DATA_DIR / "strategy_rankings" / "strategy_rankings.json").get("rankings", [])
    return {"top": r[:5]}


@router.get("/results")
def get_results(limit: int = 20):
    db = SessionLocal()
    try:
        rows = db.query(StrategyResult).order_by(StrategyResult.created_at.desc()).limit(limit).all()
        out = []
        for r in rows:
            out.append({"id": r.id, "strategy": r.strategy, "created_at": r.created_at.isoformat(), "result": r.result})
        return {"results": out}
    finally:
        db.close()


@router.post("/run")
def run_alpha_now(background: bool = True):
    """Trigger the Alpha pipeline. If `background` is true, enqueue via Celery, else run synchronously."""
    try:
        from trace_invest.tasks.alpha import run_alpha_pipeline
        if background:
            # enqueue
            res = run_alpha_pipeline.apply_async(queue="alpha")
            return {"status": "scheduled", "task_id": res.id}
        else:
            out = run_alpha_pipeline()
            return {"status": "completed", "result": out}
    except Exception as e:
        return {"error": str(e)}


@router.get("/results")
def get_results(limit: int = 20):
    db = SessionLocal()
    try:
        rows = db.query(StrategyResult).order_by(StrategyResult.created_at.desc()).limit(limit).all()
        out = []
        for r in rows:
            out.append({"id": r.id, "strategy": r.strategy, "created_at": r.created_at.isoformat(), "result": r.result})
        return {"results": out}
    finally:
        db.close()


@router.post("/run")
def run_alpha_now(background: bool = True):
    """Trigger the Alpha pipeline. If `background` is true, enqueue via Celery, else run synchronously."""
    try:
        from trace_invest.tasks.alpha import run_alpha_pipeline
        if background:
            # enqueue
            res = run_alpha_pipeline.apply_async(queue="alpha")
            return {"status": "scheduled", "task_id": res.id}
        else:
            out = run_alpha_pipeline()
            return {"status": "completed", "result": out}
    except Exception as e:
        return {"error": str(e)}
