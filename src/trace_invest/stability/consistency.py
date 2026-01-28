from typing import Dict, List
import statistics


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name or keyword.replace("_", " ") in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def _std(values):
    if len(values) < 3:
        return None
    return statistics.pstdev(values)


def analyze_consistency(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    roe_series = _extract_series(financials, "return on equity")
    margin_series = _extract_series(financials, "operating margin")

    roe_vals = []
    margin_vals = []

    for v in roe_series.values():
        try:
            roe_vals.append(float(v))
        except Exception:
            pass

    for v in margin_series.values():
        try:
            margin_vals.append(float(v))
        except Exception:
            pass

    if len(roe_vals) < 3 and len(margin_vals) < 3:
        return {
            "name": "consistency",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Not enough data for consistency analysis",
        }

    roe_std = _std(roe_vals) if len(roe_vals) >= 3 else None
    margin_std = _std(margin_vals) if len(margin_vals) >= 3 else None

    bad = 0

    if roe_std and roe_std > 0.05:
        bad += 1

    if margin_std and margin_std > 0.05:
        bad += 1

    if bad == 0:
        return {
            "name": "consistency",
            "status": "CONSISTENT",
            "risk": "LOW",
            "explanation": "ROE and margins stable across years",
        }

    if bad == 1:
        return {
            "name": "consistency",
            "status": "MODERATE",
            "risk": "MEDIUM",
            "explanation": "One profitability metric shows volatility",
        }

    return {
        "name": "consistency",
        "status": "VOLATILE",
        "risk": "HIGH",
        "explanation": "ROE and margins highly volatile",
        }

