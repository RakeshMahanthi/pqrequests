import requests_pqc

try:
    print("\n--- Testing DELETE with Classical Fallback ---")
    
    r = requests_pqc.delete("https://google.com", verify=False, pqc_mode="classical")
    
    print(f"Status: {r.status_code}")
    print(f"Curve:  {r.negotiated_curve}")
    print(f"Response: {r.content.decode('utf-8')}")
except Exception as e:
    print(f"DELETE failed: {e}")
