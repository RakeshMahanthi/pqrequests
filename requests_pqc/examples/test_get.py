import requests_pqc

# Using hybrid mode for a GET request
response = requests_pqc.get("https://localhost:5000/items", mode="classical", verify=False)

print(f"Status: {response.status_code}")
print(f"Negotiated KEM: {response.kem_algo}")
print(f"Body: {response.text[:100]}")
