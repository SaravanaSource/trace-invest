"""Alpha Factory: Phase-4 core package.
Provides top-level helpers for signal discovery, strategy generation,
ranking, monitoring and alpha scoring.
"""

from .signal_lab import signals as signal_lab
from .strategy_generator import generator as strategy_generator
from .strategy_ranking import ranker as strategy_ranker
from .strategy_monitor import monitor as strategy_monitor
from . import alpha_score

__all__ = ["signal_lab", "strategy_generator", "strategy_ranker", "strategy_monitor", "alpha_score"]
