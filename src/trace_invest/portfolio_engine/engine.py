from typing import List, Dict


def build_portfolio(decisions: List[Dict], signals: Dict[str, List[Dict]], max_position=0.15) -> Dict:
    """Deterministic portfolio constructor.

    Simple rule-based allocation:
    - Rank stocks by (conviction_score + sum(signal_strength)/100)
    - Allocate weights proportional to rank, capped by `max_position`.
    - Keep leftover as cash.
    """
    scores = []
    for d in decisions:
        sym = (d.get("symbol") or d.get("stock") or "").upper()
        conviction = float(d.get("conviction_score") or 0)
        sigs = signals.get(sym, [])
        sig_score = sum([float(s.get("signal_strength") or 0) for s in sigs]) / 100.0
        total = conviction + sig_score
        scores.append({"symbol": sym, "score": total})

    scores.sort(key=lambda r: r["score"], reverse=True)

    # Assign proportional weights but cap each at max_position
    remaining = 1.0
    positions = []
    if not scores:
        return {"portfolio_date": None, "positions": [], "cash": 1.0}

    total_score = sum([r["score"] for r in scores if r["score"] > 0])
    if total_score <= 0:
        # Defensive: no positive scores -> full cash
        return {"portfolio_date": None, "positions": [], "cash": 1.0}

    for r in scores:
        if r["score"] <= 0:
            continue
        raw_weight = r["score"] / total_score
        weight = min(raw_weight, max_position)
        positions.append({"symbol": r["symbol"], "weight": round(weight, 4)})
        remaining -= weight

    # Normalize if negative remaining due to caps
    if remaining < 0:
        # scale down pro-rata to fit 1.0
        total_alloc = sum([p["weight"] for p in positions])
        positions = [{"symbol": p["symbol"], "weight": round(p["weight"] / total_alloc * (1 - 0.0), 4)} for p in positions]
        remaining = 0.0

    return {"portfolio_date": None, "positions": positions, "cash": round(remaining, 4)}
