"""Example: Default TLS usage with PQC package helpers (placeholder)
"""
from requests_pqc import create_ssl_context, PQCSession


def main():
    ctx = create_ssl_context(verify=True)
    s = PQCSession()  # would accept ssl_opts in a real implementation
    resp = s.request("GET", "https://example.com/tls")
    print("Default TLS example response:", resp)


if __name__ == "__main__":
    main()
