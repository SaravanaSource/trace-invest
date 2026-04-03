import json

from fastapi import APIRouter, HTTPException

from trace_invest.config import data_path
from trace_invest.db import SessionLocal
from trace_invest.db.models import StrategyResult

router = APIRouter(prefix="/alpha", tags=["alpha"])
DATA_DIR = data_path()


def _read_required_json(path):
    """Return parsed JSON or raise an HTTPException with helpful detail."""
    if not path.exists():
        raise HTTPException(
            status_code=404, detail={"error": "Data not found. Run pipeline."}
        )

    try:
        return json.loads(path.read_text())
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail={"error": f"Failed to read JSON: {exc}"}
        ) from exc


@router.get("/signals")
def get_signals():
    return _read_required_json(DATA_DIR / "signals" / "signals.json")


@router.get("/strategies")
def get_strategies():
    return _read_required_json(
        DATA_DIR / "generated_strategies" / "generated_strategies.json"
    )


@router.get("/rankings")
def get_rankings():
    return _read_required_json(
        DATA_DIR / "strategy_rankings" / "strategy_rankings.json"
    )


@router.get("/monitoring")
def get_monitoring():
    return _read_required_json(
        DATA_DIR / "strategy_monitoring" / "strategy_monitoring.json"
    )


@router.get("/top")
def get_top():
    rankings = _read_required_json(
        DATA_DIR / "strategy_rankings" / "strategy_rankings.json"
    ).get("rankings", [])
    return {"top": rankings[:5]}


@router.get("/results")
def get_results(limit: int = 20):
    db = SessionLocal()
    try:
        rows = (
            db.query(StrategyResult)
            .order_by(StrategyResult.created_at.desc())
            .limit(limit)
            .all()
        )
        return {
            "results": [
                {
                    "id": row.id,
                    "strategy": row.strategy,
                    "created_at": row.created_at.isoformat(),
                    "result": row.result,
                }
                for row in rows
            ]
        }
    finally:
        db.close()


@router.post("/run")
def run_alpha_now(background: bool = True):
    """Trigger the Alpha pipeline."""
    try:
        from trace_invest.tasks.alpha import run_alpha_pipeline

        if background:
            result = run_alpha_pipeline.apply_async(queue="alpha")
            return {"status": "scheduled", "task_id": result.id}

        output = run_alpha_pipeline()
        return {"status": "completed", "result": output}
    except Exception as exc:
        return {"error": str(exc)}
