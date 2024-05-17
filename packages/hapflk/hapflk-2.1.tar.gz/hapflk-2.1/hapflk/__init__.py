"""
hapFLK : Software to infer selection from multiple population data
"""
from numpy import int16, vectorize

VERSION = "2.1"

missing = int16(-1)


def _complete_cases(x):
    return x != missing


complete_cases = vectorize(_complete_cases)


def _is_na(x):
    return x == missing


is_na = vectorize(_is_na)
