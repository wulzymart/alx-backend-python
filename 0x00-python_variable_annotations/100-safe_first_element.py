#!/usr/bin/env python3
"""Module containing safe_first_element function"""


from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Safe first element"""
    if lst:
        return lst[0]
    else:
        return None
