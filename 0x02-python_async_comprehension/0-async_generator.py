#!/usr/bin/env python3
"""Module containing async_generator"""


import asyncio
from typing import Generator
from random import uniform


async def async_generator() -> Generator[float, None, None]:
    """The coroutine will loop 10 times,
    each time asynchronously wait 1 second,
    then yield a random number between 0 and 10."""
    for i in range(10):
        await asyncio.sleep(1)
        yield uniform(0, 10)
