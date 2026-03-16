from trace_invest.validation.governance_score import compute_governance_score


def test_compute_governance_score_basic():
    details = {
        "earnings_quality": {"risk": "LOW", "status": "CLEAN"},
        "balance_sheet_stress": {"risk": "HIGH", "status": "STRESSED"},
    }

    result = compute_governance_score(details)
    assert result["governance_band"] == "MEDIUM"
    assert "balance_sheet_stress:STRESSED" in result["top_risks"]
