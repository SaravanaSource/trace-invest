from typing import Dict, List


def _extract_tax_rate_series(rows: List[Dict]) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if "tax rate" in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def analyze_tax_volatility(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    series = _extract_tax_rate_series(financials)

    if not series:
        return {
            "name": "tax_volatility",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Tax rate history unavailable",
        }

    values = []

    for v in series.values():
        try:
            if v is not None:
                values.append(float(v))
        except Exception:
            continue

    if len(values) < 3:
        return {
            "name": "tax_volatility",
            "status": "INSUFFICIENT",
            "risk": "UNKNOWN",
            "explanation": "Less than 3 years of tax rate data",
        }

    min_rate = min(values)
    max_rate = max(values)
    spread = max_rate - min_rate

    if spread < 0.05:
        return {
            "name": "tax_volatility",
            "status": "STABLE",
            "risk": "LOW",
            "explanation": "Tax rate stable across years",
        }

    if spread < 0.15:
        return {
            "name": "tax_volatility",
            "status": "MODERATE",
            "risk": "MEDIUM",
            "explanation": "Moderate variation in tax rate",
        }

    return {
        "name": "tax_volatility",
        "status": "VOLATILE",
        "risk": "HIGH",
        "explanation": "Large swings in effective tax rate",
    }

