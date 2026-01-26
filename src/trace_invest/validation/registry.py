from trace_invest.governance.earnings_quality import analyze_earnings_quality
from trace_invest.governance.unusual_items import analyze_unusual_items
from trace_invest.governance.tax_volatility import analyze_tax_volatility
from trace_invest.governance.capital_allocation import analyze_capital_allocation
from trace_invest.governance.balance_sheet_stress import analyze_balance_sheet_stress

GOVERNANCE_ENGINES = [
    analyze_earnings_quality,
    analyze_unusual_items,
    analyze_tax_volatility,
    analyze_capital_allocation,
    analyze_balance_sheet_stress,
    ]

