"""Example: Hybrid (classical + PQC) usage (placeholder)
"""
from requests_pqc import PQCSession


def main():
    s = PQCSession()
    resp = s.request("POST", "https://example.com/hybrid", data={"hello":"world"})
    print("Hybrid example response:", resp)


if __name__ == "__main__":
    main()
