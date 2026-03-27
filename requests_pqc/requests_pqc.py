import subprocess
import re

class PQCResponse:
    def __init__(self, status_code, text, kem_algo):
        self.status_code = status_code
        self.text = text
        self.kem_algo = kem_algo

    def __repr__(self):
        return f"<PQCResponse [{self.status_code}] KEM: {self.kem_algo}>"

def request(method, url, mode="classical", data=None, headers=None, verify =True, cacert=None,**kwargs):
    # Map modes to curl-compatible curve strings
    mode_map = {
        "classical": "x25519",
        "hybrid": "X25519MLKEM768",  # Note the uppercase and underscore
        "pure": "MLKEM768"
    }
    
    curve = mode_map.get(mode, "x25519")
    
    if verify == False:
        cmd = ["curl", "-s", "-v", "--curves", curve, "-k", "-X", method.upper(), url]
    else:
        cmd = ["curl", "-s", "-v", "--curves", curve, "-X", method.upper(), url]
    
    if headers:
        for k, v in headers.items():
            cmd.extend(["-H", f"{k}: {v}"])

    if verify and cacert:   
        cmd.extend(["--cacert", cacert])
    
    if data:
        # Simple string conversion for data; can be expanded for JSON
        cmd.extend(["-d", str(data)])

    # Execute curl: stdout contains the body, stderr contains headers/SSL info
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    
    # Regex parsing for status code and negotiated KEM
    status_match = re.search(r"< HTTP\/.* (\d{3})", result.stderr)
    status_code = int(status_match.group(1)) if status_match else None
    
    match = re.search(r"SSL connection using .*? / .*? / (.*?) /", result.stderr)

    if match:
        curve = match.group(1).strip()
    else:
        # Fallback: some versions might not have the trailing slash/id-ecPublicKey
        match_alt = re.search(r"SSL connection using .*? / .*? / ([^\s/]+)", result.stderr)
        curve = match_alt.group(1).strip() if match_alt else "Unknown"
    
    return PQCResponse(status_code, result.stdout, curve)

# Support for specific HTTP verbs
def get(url, **kwargs): return request("GET", url, **kwargs)
def post(url, **kwargs): return request("POST", url, **kwargs)
def put(url, **kwargs): return request("PUT", url, **kwargs)
def delete(url, **kwargs): return request("DELETE", url, **kwargs)
def patch(url, **kwargs): return request("PATCH", url, **kwargs)
