from typing import Dict, List, Optional

from trace_invest.stability.revenue_cagr import analyze_revenue_cagr
from trace_invest.stability.fcf_cagr import analyze_fcf_cagr
from trace_invest.stability.consistency import analyze_consistency
from trace_invest.stability.median_operating_margin import analyze_median_operating_margin
from trace_invest.governance.balance_sheet_stress import analyze_balance_sheet_stress

LOW_GROWTH_MAX = 0.05
MEAN_REVERTING_MAX = 0.03
POSITIVE_FCF_YEARS_REQUIRED = 2


def analyze_stability_taxonomy(processed: Dict) -> Dict:
    revenue = analyze_revenue_cagr(processed)
    fcf = analyze_fcf_cagr(processed)
    consistency = analyze_consistency(processed)
    margin = analyze_median_operating_margin(processed)
    leverage = analyze_balance_sheet_stress(processed)

    if _has_missing(revenue, fcf, consistency, margin, leverage):
        return {
            "name": "stability_taxonomy",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Insufficient data to classify stability taxonomy",
        }

    revenue_cagr = revenue.get("value")
    fcf_cagr = fcf.get("value")
    margin_status = margin.get("status")
    leverage_status = leverage.get("status")

    strong_cashflows = _has_strong_cashflows(processed)
    no_leverage_stress = leverage_status in ("STABLE", "MANAGED")

    if _is_structural_decline(revenue_cagr, fcf_cagr, margin_status):
        return {
            "name": "stability_taxonomy",
            "status": "STRUCTURAL_DECLINE",
            "risk": "HIGH",
            "explanation": "Negative growth with margin erosion",
        }

    if _is_stable_low_growth(revenue_cagr, fcf_cagr, strong_cashflows, no_leverage_stress):
        return {
            "name": "stability_taxonomy",
            "status": "STABLE_LOW_GROWTH",
            "risk": "MEDIUM",
            "explanation": "Low growth with resilient cash flows and limited leverage stress",
        }

    if _is_cyclical(revenue_cagr, fcf_cagr, consistency.get("status")):
        return {
            "name": "stability_taxonomy",
            "status": "CYCLICAL",
            "risk": "MEDIUM",
            "explanation": "Volatile results with mean-reverting growth",
        }

    return {
        "name": "stability_taxonomy",
        "status": "STABLE_LOW_GROWTH",
        "risk": "MEDIUM",
        "explanation": "No structural decline detected",
    }


def _has_missing(*items: Dict) -> bool:
    for item in items:
        status = item.get("status")
        risk = item.get("risk")
        if status in ("NO_DATA", "UNKNOWN", "ERROR", "INVALID", "INSUFFICIENT"):
            return True
        if risk == "UNKNOWN":
            return True
    return False


def _is_structural_decline(
    revenue_cagr: Optional[float],
    fcf_cagr: Optional[float],
    margin_status: Optional[str],
) -> bool:
    if revenue_cagr is None or fcf_cagr is None:
        return False
    return revenue_cagr < 0 and fcf_cagr < 0 and margin_status == "WEAK"


def _is_stable_low_growth(
    revenue_cagr: Optional[float],
    fcf_cagr: Optional[float],
    strong_cashflows: bool,
    no_leverage_stress: bool,
) -> bool:
    if revenue_cagr is None or fcf_cagr is None:
        return False

    low_growth = revenue_cagr <= LOW_GROWTH_MAX and revenue_cagr >= 0
    fcf_positive = fcf_cagr >= 0

    return low_growth and fcf_positive and strong_cashflows and no_leverage_stress


def _is_cyclical(
    revenue_cagr: Optional[float],
    fcf_cagr: Optional[float],
    consistency_status: Optional[str],
) -> bool:
    if revenue_cagr is None or fcf_cagr is None:
        return False

    mean_reverting = abs(revenue_cagr) <= MEAN_REVERTING_MAX and abs(fcf_cagr) <= MEAN_REVERTING_MAX
    volatile = consistency_status in ("VOLATILE", "MODERATE")

    return mean_reverting and volatile


def _has_strong_cashflows(processed: Dict) -> bool:
    cashflows = processed.get("cashflow") or []
    series = _extract_series(cashflows, "free cash flow")

    if not series:
        return False

    years = sorted(series.keys(), reverse=True)
    positive_years = 0

    for year in years[:3]:
        try:
            value = float(series.get(year, 0))
        except Exception:
            continue
        if value > 0:
            positive_years += 1

    return positive_years >= POSITIVE_FCF_YEARS_REQUIRED


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
