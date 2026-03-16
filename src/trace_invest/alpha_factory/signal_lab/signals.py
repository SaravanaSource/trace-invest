import json
from pathlib import Path
from statistics import stdev
from math import isfinite
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
HISTORY_DIR = DATA_DIR / "history"
SIGNALS_DIR = DATA_DIR / "signals"
SIGNALS_DIR.mkdir(parents=True, exist_ok=True)


def _load_history(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def _compute_returns(prices):
    if len(prices) < 2:
        return []
    returns = []
    for i in range(1, len(prices)):
        a = prices[i - 1]
        b = prices[i]
        if a and b and a != 0:
            returns.append((b - a) / a)
    return returns


def discover_signals(save_path: Path = None):
    """Discover signals from available history files and save JSON output.

    Output is a list of structured signals. Deterministic heuristics are used
    so the function is auditable and repeatable.
    """
    signals = []
    for f in sorted(HISTORY_DIR.glob("*.json")):
        data = _load_history(f)
        if not data:
            continue
        symbol = Path(f).stem

        # price series heuristics
        # expect a list of daily close prices at key 'close' or numeric list at top
        closes = None
        if isinstance(data, dict):
            # try common keys
            if "close" in data and isinstance(data["close"], list):
                closes = data["close"]
            elif "prices" in data and isinstance(data["prices"], list):
                # prices may be dicts
                p = data["prices"]
                if p and isinstance(p[0], dict) and "close" in p[0]:
                    closes = [d.get("close") for d in p if isinstance(d, dict) and d.get("close") is not None]
                elif all(isinstance(x, (int, float)) for x in p):
                    closes = p
        elif isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
            closes = data

        if closes and len(closes) >= 21:
            last = closes[-1]
            prev20 = closes[-21]
            momentum = (last - prev20) / prev20 if prev20 and prev20 != 0 else 0
            rets = _compute_returns(closes[-21:])
            vol = stdev(rets) if len(rets) > 1 else 0

            # deterministic thresholds
            if momentum > 0.12:
                signals.append({
                    "signal_name": "momentum_breakout",
                    "symbol": symbol,
                    "signal_strength": round(min(1.0, momentum), 4),
                    "metrics_used": ["20d_momentum"],
                    "explanation": f"20-day momentum {momentum:.3f} > 0.12",
                })

            if vol < 0.02:
                signals.append({
                    "signal_name": "volatility_drop",
                    "symbol": symbol,
                    "signal_strength": round(min(1.0, 0.02 / (vol + 1e-9)), 4),
                    "metrics_used": ["20d_volatility"],
                    "explanation": f"20-day volatility {vol:.4f} low",
                })

        # fundamentals heuristics if available
        if isinstance(data, dict) and "fundamentals" in data and isinstance(data["fundamentals"], dict):
            fnd = data["fundamentals"]
            eps_q = fnd.get("eps_quarterly") or fnd.get("eps") or []
            if isinstance(eps_q, list) and len(eps_q) >= 4:
                # check accelerating EPS across last 3 quarters
                if eps_q[-1] > eps_q[-2] > eps_q[-3]:
                    strength = min(1.0, (eps_q[-1] - eps_q[-3]) / (abs(eps_q[-3]) + 1e-9))
                    signals.append({
                        "signal_name": "earnings_acceleration",
                        "symbol": symbol,
                        "signal_strength": round(float(strength), 4),
                        "metrics_used": ["eps_quarterly"],
                        "explanation": "EPS accelerating for 3 quarters",
                    })

        # insider heuristics if field present
        if isinstance(data, dict) and "insider" in data:
            ins = data.get("insider")
            if isinstance(ins, dict) and ins.get("net_shares") and ins["net_shares"] > 0:
                signals.append({
                    "signal_name": "insider_accumulation",
                    "symbol": symbol,
                    "signal_strength": 0.6,
                    "metrics_used": ["insider.net_shares"],
                    "explanation": "insider net share purchases detected",
                })

    out = {"generated_at": datetime.utcnow().isoformat() + "Z", "signals": signals}
    target = save_path or SIGNALS_DIR / "signals.json"
    target.write_text(json.dumps(out, indent=2))
    return out
