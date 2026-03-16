from .quality_factor import quality_factor
from .value_factor import value_factor
from .growth_factor import growth_factor
from .momentum_factor import momentum_factor
from .volatility_factor import volatility_factor

__all__ = [
    "quality_factor",
    "value_factor",
    "growth_factor",
    "momentum_factor",
    "volatility_factor",
]

# Simple registry mapping canonical factor keys to functions
FACTOR_REGISTRY = {
    "value": value_factor,
    "quality": quality_factor,
    "growth": growth_factor,
    "momentum": momentum_factor,
    "volatility": volatility_factor,
}

def list_factors():
    return list(FACTOR_REGISTRY.keys())

def get_factor(name: str):
    return FACTOR_REGISTRY.get(name)
