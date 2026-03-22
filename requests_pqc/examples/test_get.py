import requests_pqc

# URL: https://httpbin.org
params = {"user": "rakesh", "mode": "pqc"}

try:
    print("--- Testing GET with Hybrid Mode ---")
    r = requests_pqc.get("https://httpbin.org", params=params, pqc_mode="hybrid")
    
    print(f"Status: {r.status_code}")
    print(f"Curve:  {r.negotiated_curve}")
    print(f"Data:   {r.json()['args']}")
except Exception as e:
    print(f"GET failed: {e}")
