import json
import requests_pqc

payload = {"item":"New Data"}

try:
    r = requests_pqc.post("https://localhost:5000/items", headers={"Content-Type": "application/json"}, data=json.dumps(payload), verify=False, mode="pure")
    
    print(f"Status: {r.status_code}")
    print(f"Curve:  {r.kem_algo}")
    print(f"Sent:   {r.text}")
except Exception as e:
    print(f"POST failed: {e}")
