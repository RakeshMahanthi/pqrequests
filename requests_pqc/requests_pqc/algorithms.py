"""Algorithm enums & validation helpers for PQC
"""
from enum import Enum
from typing import Iterable


class Algorithm(Enum):
    CLASSICAL = "classical"
    PQC = "pqc"
    HYBRID = "hybrid"


def validate_algorithm(algo: str) -> Algorithm:
    """Validate and return the matching Algorithm enum.

    Raises ValueError if not valid.
    """
    try:
        return Algorithm(algo.lower())
    except ValueError:
        valid = ", ".join(a.value for a in Algorithm)
        raise ValueError(f"Invalid algorithm '{algo}'. Valid options: {valid}")
