#!/usr/bin/env python3

from collections.abc import Iterable, Sequence
import logging
from typing import Generator

def genit(patterns: list[Iterable[str]]) -> Generator[str, None, None]:
    """Generates the combinations."""
    yield from _genit_helper("", patterns)

def _genit_helper(accumulator: str,
                  patterns: Sequence[Iterable[str]]) -> Generator[str, None, None]:
    """Recursive generator."""
    if not patterns:
        yield accumulator
        return
    car = patterns[0]
    cdr = patterns[1:]
    for caar in car:
        yield from _genit_helper(accumulator + caar, cdr)
