"""Custom exceptions for requests_pqc
"""


class PQCError(Exception):
    """Base exception for the package."""


class InvalidAlgorithmError(PQCError, ValueError):
    """Raised when an algorithm string is invalid."""
