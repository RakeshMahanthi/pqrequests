import requests_pqc

payload = {"message": "Post-Quantum Handshake", "id": 768}

try:
    print("\n--- Testing POST with Pure PQC Mode ---")
    r = requests_pqc.post("https://httpbin.org", json_data=payload, pqc_mode="pure")
    
    print(f"Status: {r.status_code}")
    print(f"Curve:  {r.negotiated_curve}")
    print(f"Sent:   {r.json()['json']}")
except Exception as e:
    print(f"POST failed: {e}")
