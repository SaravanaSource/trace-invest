from trace_invest.signal_engine.signals import compute_signals

def main():
    processed = {"financials": {"revenue_ttm": 110, "revenue_prev_ttm": 100, "fcf_ttm": 11, "fcf_prev_ttm": 9, "pe_ratio": 18, "pe_prev": 20}}
    history = {"rows": [{"conviction_score": 50}, {"conviction_score": 55}]}
    print(compute_signals(processed, history))

if __name__ == '__main__':
    main()
