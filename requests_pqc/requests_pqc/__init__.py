"""requests_pqc package

Lightweight placeholders for PQC session/adapter/ssl utilities.
"""

from .session import PQCSession
from .adapters import PQCAdapter
from .ssl_context import create_ssl_context
from .algorithms import Algorithm, validate_algorithm
from .exceptions import PQCError, InvalidAlgorithmError

__all__ = [
    "PQCSession",
    "PQCAdapter",
    "create_ssl_context",
    "Algorithm",
    "validate_algorithm",
    "PQCError",
    "InvalidAlgorithmError",
]

__version__ = "0.0.0"
