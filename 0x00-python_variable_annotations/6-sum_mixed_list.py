#!/usr/bin/env python3
"""Module containing sum mixed list"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """sums a mixed list of integers and floats"""
    return float(sum(mxd_lst))
