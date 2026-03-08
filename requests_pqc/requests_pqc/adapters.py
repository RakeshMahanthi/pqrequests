"""PQC adapter primitives

Provide a minimal adapter abstraction with a `send` method.
"""
from typing import Any


class PQCAdapter:
    """A very small adapter placeholder.

    The real adapter would handle connection setup, request encoding, and PQC-specific
    handshake details. This placeholder just captures the interface.
    """

    def send(self, method: str, url: str, **kwargs) -> Any:
        """Pretend to send a request and return a dummy response dict."""
        return {
            "method": method,
            "url": url,
            "kwargs": kwargs,
            "status": 200,
            "body": "(placeholder response)"
        }
