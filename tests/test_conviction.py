from trace_invest.intelligence.conviction import conviction_score


def test_conviction_score_components():
    validation_result = {
        "master": {"master_band": "AVERAGE"},
        "governance": {"governance_band": "LOW"},
        "stability": {"stability_band": "AVERAGE"},
        "details": {"valuation_sanity": {"status": "REASONABLE"}},
        "data_confidence_score": 90,
        "data_confidence_band": "HIGH",
    }

    result = conviction_score({}, validation_result)
    assert result["conviction_score"] == 69
    assert result["components"]["valuation_sanity"] == "REASONABLE"
