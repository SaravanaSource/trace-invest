import json
from pathlib import Path
from datetime import datetime
from typing import List

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
SIGNALS_FILE = DATA_DIR / "signals" / "signals.json"
OUT_DIR = DATA_DIR / "generated_strategies"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _load_signals():
    if not SIGNALS_FILE.exists():
        return []
    return json.loads(SIGNALS_FILE.read_text()).get("signals", [])


def _rule_for_signal(sig: dict) -> str:
    name = sig.get("signal_name", "")
    symbol = sig.get("symbol", "")
    if name == "momentum_breakout":
        return "momentum_score > 0.7"
    if name == "earnings_acceleration":
        return "eps_growth_quarterly > 0.1"
    if name == "insider_accumulation":
        return "insider_net_buy > 0"
    if name == "volatility_drop":
        return "volatility_20d < 0.02"
    return f"has_signal_{name} == true"


def generate_strategies(save_path: Path = None, max_strategies: int = 10):
    signals = _load_signals()
    # group signals by name and pick deterministic ordering
    signals_sorted = sorted(signals, key=lambda s: (s.get("signal_name"), -s.get("signal_strength", 0)))
    strategies = []
    # deterministic strategy generation: combine adjacent pairs of signals
    for i in range(0, min(len(signals_sorted), max_strategies * 2), 2):
        a = signals_sorted[i]
        if i + 1 < len(signals_sorted):
            b = signals_sorted[i + 1]
        else:
            b = None
        name_parts = [a.get("signal_name")]
        rules = [ _rule_for_signal(a) ]
        if b:
            name_parts.append(b.get("signal_name"))
            rules.append(_rule_for_signal(b))

        strat_name = "_".join(name_parts)
        strat = {
            "strategy_name": strat_name,
            "rules": rules,
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        strategies.append(strat)

    out = {"generated_at": datetime.utcnow().isoformat() + "Z", "strategies": strategies}
    target = save_path or OUT_DIR / "generated_strategies.json"
    target.write_text(json.dumps(out, indent=2))
    return out
