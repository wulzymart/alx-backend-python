#!/usr/bin/env python3
"""Module containing wait random"""

import asyncio
from random import uniform


async def wait_random(max_delay: int = 10) -> float:
    """waits for a random delay between 0 and max_delay
      seconds and eventually returns it."""
    delay = uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
