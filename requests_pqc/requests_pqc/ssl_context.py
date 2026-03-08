"""SSL context creation helpers

Provide a tiny helper to create an ssl.SSLContext (placeholder behaviour).
"""
import ssl
from typing import Optional


def create_ssl_context(verify: bool = True, protocol: Optional[str] = None) -> ssl.SSLContext:
    """Return a configured SSLContext.

    Args:
        verify: whether to verify certificates
        protocol: optional protocol string (unused in this placeholder)
    """
    ctx = ssl.create_default_context()
    if not verify:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx
