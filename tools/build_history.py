from pathlib import Path
from trace_invest.company_history_engine import build_company_history
from trace_invest.config.loader import load_config


def main():
    cfg = load_config()
    universe = cfg.get("universe", {}).get("universe", {})
    stocks = universe.get("stocks") or []
    if not stocks:
        print("No stocks in universe")
        return

    for s in stocks:
        sym = s.get("symbol")
        if not sym:
            continue
        print("Building history for", sym)
        build_company_history(sym)

if __name__ == '__main__':
    main()
