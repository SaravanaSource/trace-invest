from typing import Dict, Any, List
from pathlib import Path
import json

ROOT = Path("data/strategies")
ROOT.mkdir(parents=True, exist_ok=True)


def _eval_rule(rule: str, processed: Dict) -> bool:
    """Evaluate a simple rule like 'ROE > 18' against processed financials.

    Allowed identifiers map to keys in `processed['financials']`. This is
    intentionally minimal and deterministic.
    """
    fin = processed.get("financials", {}) or {}
    # map common names
    mapping = {
        "ROE": fin.get("roe") or fin.get("roe_ttm"),
        "revenue_growth": fin.get("revenue_growth") or fin.get("revenue_growth_pct") or fin.get("revenue_ttm"),
        "debt_to_equity": fin.get("debt_to_equity") or fin.get("debt_equity_ratio"),
        "valuation_reasonable": fin.get("pe_ratio") is not None,
    }
    # simple parser: split on spaces
    parts = rule.split()
    if len(parts) == 3:
        left, op, right = parts
        left_val = mapping.get(left) if left in mapping else fin.get(left.lower())
        try:
            if isinstance(left_val, bool):
                if op == "==":
                    return str(left_val).lower() == right.lower()
                return False
            if left_val is None:
                return False
            rv = float(right)
            lv = float(left_val)
            if op == ">":
                return lv > rv
            if op == ">=":
                return lv >= rv
            if op == "<":
                return lv < rv
            if op == "<=":
                return lv <= rv
            if op == "==":
                return lv == rv
        except Exception:
            return False
    # fallback: rule like 'valuation_reasonable = true'
    if "=" in rule:
        k, v = [p.strip() for p in rule.split("=")]
        val = mapping.get(k) if k in mapping else fin.get(k)
        if isinstance(val, bool):
            return str(val).lower() == v.lower()
        return False

    return False


def run_strategy(strategy: Dict[str, Any], universe: List[Dict]) -> List[Dict]:
    """Run a strategy (dict) against an in-memory universe of processed stocks.

    `universe` is list of {symbol, processed, history}
    Outputs a ranked list saved to `data/strategies/<name>/results.json`.
    """
    name = strategy.get("name") or "unnamed"
    rules = strategy.get("rules", [])
    ranking = strategy.get("ranking", {})
    top_n = ranking.get("top_n", 50)

    rows = []
    for item in universe:
        sym = item.get("symbol")
        processed = item.get("processed", {})
        ok = True
        for r in rules:
            if not _eval_rule(r, processed):
                ok = False
                break
        if ok:
            # simple score: sum of factors we can find
            score = 0.0
            fin = processed.get("financials", {}) or {}
            try:
                score += float(fin.get("roe") or fin.get("roe_ttm") or 0)
            except Exception:
                pass
            rows.append({"symbol": sym, "score": round(score, 4), "reason": f"passed {len(rules)} rules"})

    rows.sort(key=lambda r: r["score"], reverse=True)
    out = rows[:top_n]

    out_dir = ROOT / name.replace(" ", "_")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "results.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out
from pathlib import Path
import json
from typing import Dict, Any, List

from trace_invest.data_ingestion.financials_fetcher import fetch_financials_from_local

SNAPSHOT_DIR = Path("data/snapshots")
OUT_DIR = Path("data/strategies")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _load_latest_snapshot():
    dates = sorted([d.name for d in SNAPSHOT_DIR.iterdir() if d.is_dir()])
    if not dates:
        return {}
    p = SNAPSHOT_DIR / dates[-1] / "snapshot.json"
    return json.loads(p.read_text(encoding="utf-8"))


def _apply_rule(financials: Dict[str, Any], rule: str) -> bool:
    # Very small rule parser: support `KEY OP VALUE` where OP is one of >,<,>=,<=,=
    parts = rule.split()
    if len(parts) != 3:
        return False
    key, op, val = parts
    key = key.lower()
    try:
        fv = float(financials.get(key) or financials.get(key.upper()) or 0)
        vv = float(val)
    except Exception:
        return False

    if op == ">":
        return fv > vv
    if op == "<":
        return fv < vv
    if op == ">=":
        return fv >= vv
    if op == "<=":
        return fv <= vv
    if op == "=":
        return fv == vv
    return False


def run_strategy(strategy_def: Dict[str, Any]) -> Dict[str, Any]:
    """Run a strategy definition and persist results.

    strategy_def example:
    {
      "name": "Quality Growth",
      "rules": ["roe > 18", "revenue_growth > 15"],
      "ranking": {"top_n": 20}
    }
    """
    snap = _load_latest_snapshot()
    decisions = snap.get("decisions", [])

    candidates: List[Dict[str, Any]] = []
    for d in decisions:
        sym = (d.get("symbol") or d.get("stock") or "").upper()
        fin = fetch_financials_from_local(sym) or {}
        flat = fin.get("financials", {})
        # apply all rules
        ok = True
        for r in strategy_def.get("rules", []):
            if not _apply_rule(flat, r):
                ok = False
                break
        if ok:
            # ranking metric: use conviction_score if present
            score = float(d.get("conviction_score") or 0)
            candidates.append({"symbol": sym, "score": score, "reasoning": d})

    candidates.sort(key=lambda x: x["score"], reverse=True)
    top_n = strategy_def.get("ranking", {}).get("top_n", 20)
    out = candidates[:top_n]

    sname = strategy_def.get("name", "unnamed").replace(" ", "_")
    outpath = OUT_DIR / sname / "results.json"
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(json.dumps({"strategy": strategy_def.get("name"), "count": len(out), "rows": out}, indent=2), encoding="utf-8")

    return {"strategy": strategy_def.get("name"), "count": len(out), "rows": out}
