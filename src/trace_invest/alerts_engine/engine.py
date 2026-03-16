from typing import List, Dict
from datetime import datetime, timezone


def generate_alerts(decisions: List[Dict], prev_decisions_map: Dict[str, Dict], signals_map: Dict[str, List[Dict]]) -> List[Dict]:
    """Generate deterministic alerts based on conviction deltas, governance, and signals.

    `prev_decisions_map` keyed by symbol for quick lookup.
    """
    alerts: List[Dict] = []
    ts = datetime.now(timezone.utc).isoformat()

    for d in decisions:
        sym = (d.get("symbol") or d.get("stock") or "").upper()
        prev = prev_decisions_map.get(sym)
        # Conviction change alert
        try:
            curr_score = float(d.get("conviction_score") or 0)
            prev_score = float(prev.get("conviction_score") or 0) if prev else 0.0
            if curr_score - prev_score >= 10:
                alerts.append({"alert_type": "conviction_increase", "symbol": sym, "severity": "medium", "reason": f"Conviction +{curr_score - prev_score}", "timestamp": ts})
            if prev and prev_score - curr_score >= 10:
                alerts.append({"alert_type": "conviction_decrease", "symbol": sym, "severity": "medium", "reason": f"Conviction -{prev_score - curr_score}", "timestamp": ts})
        except Exception:
            pass

        # Governance deterioration
        gov = d.get("governance", {})
        if gov and gov.get("governance_band") == "HIGH":
            alerts.append({"alert_type": "governance_warning", "symbol": sym, "severity": "high", "reason": "Governance band HIGH", "timestamp": ts})

        # New strong signals
        sigs = signals_map.get(sym, [])
        for s in sigs:
            if float(s.get("signal_strength") or 0) >= 20:
                alerts.append({"alert_type": "opportunity_signal", "symbol": sym, "severity": "low", "reason": s.get("explanation"), "timestamp": ts})

    return alerts
