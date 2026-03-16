from trace_invest.validation.runner import run_validation


def test_run_validation_smoke():
    # Provide minimal processed data; run_validation must return stable structure
    processed = {"financials": {}}
    result = run_validation(processed)

    assert "total_flags" in result
    assert "overall_risk" in result
    assert "details" in result and isinstance(result["details"], dict)
    assert "governance" in result and isinstance(result["governance"], dict)
    assert "stability" in result and isinstance(result["stability"], dict)
    assert "master" in result and isinstance(result["master"], dict)
