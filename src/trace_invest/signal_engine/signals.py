from typing import Dict, List


def compute_signals(processed: Dict, history: Dict) -> List[Dict]:
    """Compute simple deterministic signals for a stock.

    Signals are rule-based and reproducible.
    """
    signals: List[Dict] = []

    fin = processed.get("financials", {})

    # Example: revenue acceleration
    revenue = fin.get("revenue_ttm")
    revenue_prev = fin.get("revenue_prev_ttm") or fin.get("revenue_prev")
    if isinstance(revenue, (int, float)) and isinstance(revenue_prev, (int, float)):
        # treat >=10% growth as acceleration (deterministic boundary)
        # use tolerant comparison to avoid floating-point rounding issues
        if revenue_prev > 0 and (revenue / float(revenue_prev)) >= (1.1 - 1e-9):
            signals.append({
                "signal_name": "revenue_acceleration",
                "signal_strength": round((revenue / revenue_prev - 1) * 100, 2),
                "explanation": "Revenue grew >10% vs prior period",
                "metrics": {"revenue": revenue, "revenue_prev": revenue_prev},
            })

    # Example: free cash flow improvement
    fcf = fin.get("fcf_ttm")
    fcf_prev = fin.get("fcf_prev_ttm") or fin.get("fcf_prev")
    if isinstance(fcf, (int, float)) and isinstance(fcf_prev, (int, float)):
        if fcf_prev != 0 and fcf > fcf_prev:
            signals.append({
                "signal_name": "fcf_improving",
                "signal_strength": round((fcf / max(1e-9, fcf_prev) - 1) * 100, 2),
                "explanation": "Free cash flow improved vs prior period",
                "metrics": {"fcf": fcf, "fcf_prev": fcf_prev},
            })

    # Example: valuation compression (PE drop)
    pe = fin.get("pe_ratio")
    pe_prev = fin.get("pe_prev")
    if isinstance(pe, (int, float)) and isinstance(pe_prev, (int, float)):
        if pe_prev > 0 and pe < pe_prev:
            signals.append({
                "signal_name": "valuation_compression",
                "signal_strength": round((pe_prev - pe) / pe_prev * 100, 2),
                "explanation": "PE compressed vs previous period",
                "metrics": {"pe": pe, "pe_prev": pe_prev},
            })

    # Use history to detect rising conviction
    rows = history.get("rows", []) if isinstance(history, dict) else []
    if len(rows) >= 2:
        try:
            last = float(rows[-1].get("conviction_score") or 0)
            prev = float(rows[-2].get("conviction_score") or 0)
            if prev > 0 and last > prev:
                signals.append({
                    "signal_name": "conviction_rising",
                    "signal_strength": round(last - prev, 2),
                    "explanation": "Conviction score increased vs previous snapshot",
                    "metrics": {"last": last, "prev": prev},
                })
        except Exception:
            pass

    return signals


def rank_opportunities(signals_map: Dict[str, List[Dict]]) -> List[Dict]:
    """Score and rank symbols by aggregated signal strength.

    Input: mapping symbol -> list of signals
    Output: list of {symbol, score, signals}
    """
    rows = []
    for sym, sigs in signals_map.items():
        score = 0.0
        for s in sigs:
            score += float(s.get("signal_strength") or 0)
        rows.append({"symbol": sym, "score": round(score, 2), "signals": sigs})

    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows
