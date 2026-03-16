from trace_invest.signal_engine.signals import compute_signals, rank_opportunities


def test_compute_signals_and_rank():
    processed = {"financials": {"revenue_ttm": 110, "revenue_prev_ttm": 100, "fcf_ttm": 11, "fcf_prev_ttm": 9, "pe_ratio": 18, "pe_prev": 20}}
    history = {"rows": [{"conviction_score": 50}, {"conviction_score": 55}]}

    sigs = compute_signals(processed, history)
    assert any(s["signal_name"] == "revenue_acceleration" for s in sigs)
    assert any(s["signal_name"] == "fcf_improving" for s in sigs)

    mapping = {"ABC": sigs}
    ranked = rank_opportunities(mapping)
    assert ranked[0]["symbol"] == "ABC"
