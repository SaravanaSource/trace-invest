from pathlib import Path
import json
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
OUT_DIR = DATA_DIR / "insights"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_insights(save_path: Path = None):
    # Simple deterministic insights based on signals and market prices
    sig_file = DATA_DIR / "signals" / "signals.json"
    prices_file = DATA_DIR / "market_prices.json"
    sigs = []
    if sig_file.exists():
        try:
            sigs = json.loads(sig_file.read_text()).get("signals", [])
        except Exception:
            sigs = []
    prices = {}
    if prices_file.exists():
        try:
            prices = json.loads(prices_file.read_text())
        except Exception:
            prices = {}

    insights = []
    # Top momentum signals
    top = sorted([s for s in sigs if s.get("signal_name") == "momentum_breakout"], key=lambda x: -x.get("signal_strength", 0))[:10]
    for s in top:
        sym = s.get("symbol")
        p = prices.get(sym, {}).get("last_price")
        insights.append({"type": "opportunity", "symbol": sym, "reason": s.get("explanation"), "price": p})

    out = {"generated_at": datetime.utcnow().isoformat()+"Z", "insights": insights}
    target = save_path or OUT_DIR / "insights.json"
    target.write_text(json.dumps(out, indent=2))
    return out
