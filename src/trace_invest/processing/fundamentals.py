from typing import Dict


def compute_quality_metrics(raw: Dict) -> Dict:
    info = raw.get("info", {})

    return {
        "roe": info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0,
        "debt_to_equity": info.get("debtToEquity", 0) / 100 if info.get("debtToEquity") else 0,
        "operating_margin": info.get("operatingMargins", 0) * 100 if info.get("operatingMargins") else 0,
        "revenue_growth_5y": info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else 0,
    }


def compute_valuation_metrics(raw: Dict) -> Dict:
    info = raw.get("info", {})

    return {
        "pe_ratio": info.get("trailingPE"),
        "pb_ratio": info.get("priceToBook"),
        "fcf_yield": (
            (info.get("freeCashflow") / info.get("marketCap") * 100)
            if info.get("freeCashflow") and info.get("marketCap")
            else 0
        ),
    }


def build_processed_fundamentals(raw: Dict) -> Dict:
    return {
        "quality_metrics": compute_quality_metrics(raw),
        "valuation_metrics": compute_valuation_metrics(raw),
        "financials": {},    # extend later
        "governance": {},    # extend later
    }

