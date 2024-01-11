#!/usr/bin/env python3
"""Module containing sum list"""


from typing import List


def sum_list(input_list: List[float]) -> float:
    """sums a mixed list"""
    sum: float = 0.0
    for x in input_list:
        sum += x
    return sum
