from trace_invest.valuation.sanity import analyze_valuation_sanity


def test_valuation_rich():
    processed = {"valuation_metrics": {"pe_ratio": 50, "pb_ratio": 2, "fcf_yield": 0.03}}
    result = analyze_valuation_sanity(processed)
    assert result["status"] == "RICH"
    assert result["risk"] == "MEDIUM"
