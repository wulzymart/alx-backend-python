#!/usr/bin/env python3
"""Module containing element_length function"""

from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """returns list of tuples of sequence and its lengths"""
    return [(i, len(i)) for i in lst]
