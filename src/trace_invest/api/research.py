from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter(prefix="/research", tags=["research"])

BASE = Path("data")


@router.get("/strategies")
def list_strategies():
    p = BASE / "strategies"
    if not p.exists():
        return {"strategies": []}
    out = []
    for d in sorted(p.iterdir()):
        if not d.is_dir():
            continue
        f = d / "results.json"
        if f.exists():
            try:
                out.append({"name": d.name, "results": json.loads(f.read_text(encoding="utf-8"))})
            except Exception:
                out.append({"name": d.name, "error": "invalid results"})
        else:
            out.append({"name": d.name, "results": None})
    return {"strategies": out}


@router.get("/backtests")
def list_backtests():
    p = BASE / "backtests"
    if not p.exists():
        return {"backtests": []}
    out = []
    for f in sorted(p.glob("*.json")):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            out.append({"file": f.name, "error": "invalid json"})
    return {"backtests": out}


@router.get("/performance")
def list_performance():
    p = BASE / "performance_reports"
    if not p.exists():
        return {"performance": []}
    out = []
    for f in sorted(p.glob("*.json")):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            out.append({"file": f.name, "error": "invalid json"})
    return {"performance": out}


@router.get("/factors")
def list_factors():
    p = BASE / "factors"
    if not p.exists():
        return {"factors": []}
    out = []
    for f in sorted(p.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            out.append({"symbol": f.stem, "factors": data})
        except Exception:
            out.append({"file": f.name, "error": "invalid json"})
    return {"factors": out}
