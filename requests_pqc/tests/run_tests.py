"""Quick smoke test for requests_pqc package

This script does not rely on pytest; it runs a small import & instantiation test so it's easy
to run in most environments.
"""
import os
import sys

# Ensure the package directory is importable (parent of this tests/ directory)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from requests_pqc import PQCSession, PQCAdapter, create_ssl_context, validate_algorithm


def main():
    # Basic import/instantiation smoke checks
    s = PQCSession()
    adapter = PQCAdapter()
    assert isinstance(s.adapter, PQCAdapter)
    resp = s.request("GET", "https://example.test/")
    assert isinstance(resp, dict)

    ctx = create_ssl_context()
    assert ctx is not None

    algo = validate_algorithm("pqc")
    assert algo.name.lower() in ("pqc",)

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
