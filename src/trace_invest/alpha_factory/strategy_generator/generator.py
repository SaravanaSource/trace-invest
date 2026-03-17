import json
from pathlib import Path
from datetime import datetime
from typing import List

from trace_invest.config import data_path, ensure_data_dirs

ensure_data_dirs("signals", "generated_strategies")
SIGNALS_FILE = data_path("signals", "signals.json")
OUT_DIR = data_path("generated_strategies")
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
    # deterministic strategy generation: combine signals from different symbols
    # iterate signals and pair each with the next signal that has a different symbol
    i = 0
    while len(strategies) < max_strategies and i < len(signals_sorted):
        a = signals_sorted[i]
        # find next signal with different symbol
        b = None
        for j in range(i + 1, len(signals_sorted)):
            if signals_sorted[j].get("symbol") != a.get("symbol"):
                b = signals_sorted[j]
                break
        name_parts = [a.get("signal_name")]
        rules = [ _rule_for_signal(a) ]
        if b:
            name_parts.append(b.get("signal_name"))
            rules.append(_rule_for_signal(b))

        strat_name = "_".join(name_parts)
        # derive deterministic positions from the signals used
        positions = []
        symbols = [a.get("symbol")]
        if b:
            symbols.append(b.get("symbol"))
        # equal weight positions with attached reasoning
        weight = round(1.0 / len(symbols), 4) if symbols else 0.0
        for s in symbols:
            positions.append({"symbol": s, "weight": weight, "reasoning": {"from_signals": True}})

        strat = {
            "strategy_name": strat_name,
            "rules": rules,
            "positions": positions,
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        strategies.append(strat)
        # advance pointer; if we used b at j, skip to j+1 to avoid repeated reuse
        if b:
            i = j + 1
        else:
            i += 1

    out = {"generated_at": datetime.utcnow().isoformat() + "Z", "strategies": strategies}
    target = save_path or OUT_DIR / "generated_strategies.json"
    target.write_text(json.dumps(out, indent=2))
    return out
