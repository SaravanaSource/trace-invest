from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(prefix="/research", tags=["research"])


@router.get("/strategies")
def list_strategies():
    # list available strategy result folders
    from pathlib import Path
    root = Path("data/strategies")
    if not root.exists():
        return []
    return [p.name for p in root.iterdir() if p.is_dir()]


@router.get("/strategies/{name}")
def get_strategy_results(name: str):
    from pathlib import Path
    import json
    p = Path("data/strategies") / name / "results.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail="strategy not found")
    return json.loads(p.read_text(encoding="utf-8"))


@router.get("/backtests/{name}")
def get_backtest(name: str):
    from pathlib import Path
    import json
    p = Path("data/backtests") / f"{name}.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail="backtest not found")
    return json.loads(p.read_text(encoding="utf-8"))


@router.get("/factors")
def list_factors():
    # simple listing of factor modules
    return ["quality_roe", "value_inv_pe", "growth_revenue_pct", "momentum_pct", "volatility_annual_pct"]


@router.get("/performance/{name}")
def get_performance(name: str):
    from pathlib import Path
    import json
    p = Path("data/performance_reports") / f"{name}.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail="performance report not found")
    return json.loads(p.read_text(encoding="utf-8"))


@router.get("/query/top_conviction_growth")
def top_conviction_growth():
    from trace_invest.research.research_assistant.assistant import top_conviction_growth
    return top_conviction_growth(2, 20)
from fastapi import APIRouter, HTTPException
from typing import Dict
from pathlib import Path
import json

router = APIRouter(prefix="/research", tags=["research"])


@router.get("/strategies")
def list_strategies():
    base = Path("data/strategies")
    out = []
    if not base.exists():
        return out
    for s in base.iterdir():
        if s.is_dir():
            out.append(s.name)
    return out


@router.get("/strategies/{name}")
def get_strategy_results(name: str):
    p = Path("data/strategies") / name / "results.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail="strategy not found")
    return json.loads(p.read_text(encoding="utf-8"))


@router.get("/backtests/{name}")
def get_backtest(name: str):
    p = Path("data/backtests") / f"{name}.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail="backtest not found")
    return json.loads(p.read_text(encoding="utf-8"))


@router.get("/factors")
def list_factors():
    return ["quality", "value", "growth", "momentum", "volatility"]


@router.get("/research/query")
def research_query(q: str):
    from trace_invest.research.research_assistant.assistant import answer_query
    return answer_query(q)
