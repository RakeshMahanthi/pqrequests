"""PQC session wrapper

Contains a small PQCSession class that orchestrates an adapter and SSL context.
"""
from typing import Optional

from .adapters import PQCAdapter
from .ssl_context import create_ssl_context
from .exceptions import PQCError


class PQCSession:
    """Simple PQC session placeholder.

    Args:
        adapter: an instance of PQCAdapter (or subclass)
        ssl_opts: dict passed to create_ssl_context
    """

    def __init__(self, adapter: Optional[PQCAdapter] = None, **ssl_opts):
        self.adapter = adapter or PQCAdapter()
        self.ssl_context = create_ssl_context(**ssl_opts)

    def request(self, method: str, url: str, **kwargs):
        """Send a request using the configured adapter.

        This is a placeholder API to illustrate how the package pieces fit together.
        """
        if not self.adapter:
            raise PQCError("No adapter configured")
        return self.adapter.send(method, url, ssl_context=self.ssl_context, **kwargs)
