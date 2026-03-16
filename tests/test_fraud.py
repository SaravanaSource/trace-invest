from trace_invest.validation.fraud import check_basic_fraud_flags


def test_fraud_flag_cash_flow_mismatch():
    financials = {"cash_flow_from_ops": -10, "net_profit": 10, "receivables_growth_pct": 5, "related_party_txn_pct": 1}
    result = check_basic_fraud_flags(financials)
    assert result["flag_count"] >= 1
    assert result["risk_level"] in ("MEDIUM", "HIGH")
