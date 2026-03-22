import requests_pqc

# URL for testing (Use a server supporting X25519MLKEM768)
TEST_URL = "https://www.google.com" 

try:
    print(f"Connecting to {TEST_URL} in Hybrid Mode...")
    r = requests_pqc.get(TEST_URL, pqc_mode="hybrid")
    
    print("-" * 30)
    print(f"Status Code: {r.status_code}")
    print(f"Negotiated Curve: {r.negotiated_curve}")
    print(f"Response Snippet: {r.text()[:50]}...")
    print("-" * 30)

except Exception as e:
    print(f"Error: {e}")
