from typing import Dict, Any
import json
from pathlib import Path

OUT = Path("data/performance_reports")
OUT.mkdir(parents=True, exist_ok=True)


def analyze_backtest(backtest_result: Dict[str, Any]) -> Dict[str, Any]:
    # For now, simply mirror fields and add a basic rating
    cagr = backtest_result.get("CAGR", 0)
    vol = backtest_result.get("volatility", 0)
    sharpe = backtest_result.get("sharpe_ratio", 0)
    rating = "neutral"
    if sharpe >= 1.0:
        rating = "good"
    if sharpe >= 1.5:
        rating = "excellent"

    report = {"summary": {"CAGR": cagr, "volatility": vol, "sharpe": sharpe, "rating": rating}, "detail": backtest_result}
    out = OUT / f"{backtest_result.get('strategy')}_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
