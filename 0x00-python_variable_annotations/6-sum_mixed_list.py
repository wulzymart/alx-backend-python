#!/usr/bin/env python3
"""Module containing sum mixed list"""


from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[float, int]]) -> float:
    """sums a mixed list of integers and floats"""
    sum: float = 0.0
    for x in mxd_lst:
        sum += x
    return sum
