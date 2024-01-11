#!/usr/bin/env python3
"""Module containing to_kv function"""

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """reurns turple k, v"""
    return (k, float(v))
