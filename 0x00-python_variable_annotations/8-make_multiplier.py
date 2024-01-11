#!/usr/bin/env python3
"""Module containing tmake_multiplier function"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """returns a multiplierction"""

    def multiplier_fn(x: float) -> float:
        return multiplier * x

    return multiplier_fn
