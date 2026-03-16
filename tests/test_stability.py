from trace_invest.stability.stability_score import compute_stability_score


def test_stability_taxonomy_override():
    details = {
        "revenue_cagr": {"risk": "HIGH", "status": "DECLINING"},
        "stability_taxonomy": {"status": "STRUCTURAL_DECLINE"},
    }

    result = compute_stability_score(details)
    assert result["stability_band"] == "WEAK"
    assert "stability_taxonomy:STRUCTURAL_DECLINE" in result["weak_areas"]
