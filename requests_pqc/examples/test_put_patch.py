import requests_pqc

try:
    print("\n--- Testing PUT and PATCH with Hybrid Mode ---")
    
    # PUT Example
    r_put = requests_pqc.put("https://httpbin.org", data="Raw update string", pqc_mode="hybrid")
    print(f"PUT Status: {r_put.status_code} | Curve: {r_put.negotiated_curve}")

    # PATCH Example
    r_patch = requests_pqc.patch("https://httpbin.org", json_data={"patch": "partial"}, pqc_mode="hybrid")
    print(f"PATCH Status: {r_patch.status_code} | Curve: {r_patch.negotiated_curve}")
    
except Exception as e:
    print(f"Update failed: {e}")
