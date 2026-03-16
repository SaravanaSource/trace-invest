from trace_invest.outputs.signals import conviction_to_zone, generate_signal


def test_conviction_to_zone_boundaries():
    assert conviction_to_zone(90) == "STRONG_BUY"
    assert conviction_to_zone(75) == "BUY"
    assert conviction_to_zone(60) == "HOLD"
    assert conviction_to_zone(45) == "CAUTION"
    assert conviction_to_zone(10) == "AVOID"


def test_generate_signal_low_confidence_adjustment():
    conviction_result = {
        "conviction_score": 30,
        "overall_risk": "HIGH",
        "components": {},
        "risk_penalty": 0,
        "data_confidence_band": "LOW",
    }

    sig = generate_signal(conviction_result)
    assert sig["zone"] == "HOLD"
