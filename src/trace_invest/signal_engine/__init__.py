"""Signal discovery engine for Phase-2.

Provides deterministic signal computations from processed fundamentals and history.
"""

from .signals import compute_signals, rank_opportunities

__all__ = ["compute_signals", "rank_opportunities"]
