"""Example: PQC-only usage (placeholder)
"""
from requests_pqc import PQCSession


def main():
    s = PQCSession()
    resp = s.request("GET", "https://example.com/pqc")
    print("PQC-only example response:", resp)


if __name__ == "__main__":
    main()
