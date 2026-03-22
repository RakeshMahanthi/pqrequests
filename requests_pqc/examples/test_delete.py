import requests_pqc

try:
    print("\n--- Testing DELETE with Classical Fallback ---")
    headers = {"Authorization": "Bearer PQC_TOKEN_123"}
    
    r = requests_pqc.delete("https://httpbin.org", headers=headers, pqc_mode="classical")
    
    print(f"Status: {r.status_code}")
    print(f"Curve:  {r.negotiated_curve}")
except Exception as e:
    print(f"DELETE failed: {e}")
