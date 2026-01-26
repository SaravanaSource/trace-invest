from trace_invest.stability.median_roe import analyze_median_roe
from trace_invest.stability.median_operating_margin import analyze_median_operating_margin
from trace_invest.stability.revenue_cagr import analyze_revenue_cagr
from trace_invest.stability.fcf_cagr import analyze_fcf_cagr
from trace_invest.stability.consistency import analyze_consistency


STABILITY_ENGINES = [
    analyze_median_roe,
    analyze_median_operating_margin,
    analyze_revenue_cagr,
    analyze_fcf_cagr,
    analyze_consistency,
]

