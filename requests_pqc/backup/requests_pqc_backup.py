import pycurl
import ctypes
import re
import json
from ctypes.util import find_library
from io import BytesIO

# libcurl numeric for CURLOPT_SSL_EC_CURVES
CURL_OPT_SSL_EC_CURVES = 10298

class Response:
    """Mirrors the requests.Response object."""
    def __init__(self, content, status_code, headers, negotiated_curve=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers
        self.negotiated_curve = negotiated_curve
    
    def text(self):
        return self.content.decode('utf-8', errors='replace')

    def json(self):
        return json.loads(self.text())

class Session:
    def __init__(self):
        # Locate the libcurl binary for direct C-level calls
        lib_path = find_library('curl')
        if not lib_path:
            raise ImportError("Could not find libcurl. Ensure it is installed.")
        self.libcurl = ctypes.CDLL(lib_path)
        
        # Mapping PQC Modes to OpenSSL groups (verified for OpenSSL 3.6.1)
        self.modes = {
            "classical": "X25519",           # Standard 
            "hybrid":    "X25519MLKEM768",  # Note the UNDERSCORE (_)
            "pure":      "MLKEM768"          # Standard NIST name
        }


    def request(self, method, url, data=None, json_data=None, pqc_mode="classical", timeout=30, verify=True):
        buffer = BytesIO()
        header_buffer = BytesIO()
        debug_logs = []

        def debug_callback(infotype, message):
            debug_logs.append(message.decode('utf-8', errors='ignore'))

        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.CUSTOMREQUEST, method.upper())
        c.setopt(pycurl.WRITEDATA, buffer)
        c.setopt(pycurl.HEADERFUNCTION, header_buffer.write)
        c.setopt(pycurl.TIMEOUT, timeout)
        
        # Enable log capturing for curve verification
        c.setopt(pycurl.VERBOSE, True)
        c.setopt(pycurl.DEBUGFUNCTION, debug_callback)

        if verify:
            c.setopt(pycurl.SSL_VERIFYPEER, True)
            c.setopt(pycurl.SSL_VERIFYHOST, 2)
        else:
            c.setopt(pycurl.SSL_VERIFYPEER, False)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
            
        # Handle POST Data
        if json_data:
            c.setopt(pycurl.POSTFIELDS, json.dumps(json_data))
            c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
        elif data:
            c.setopt(pycurl.POSTFIELDS, data)

        # 1. Prepare the curve string
        selected_curve = self.modes.get(pqc_mode, "X25519")
        raw_curve_string = selected_curve.encode('utf-8')

        # 2. Get the RAW C POINTER to the curl handle correctly
        # In modern PycURL, this is the safest way to get the handle for ctypes
        try:
            # Try to get handle directly if available
            handle_ptr = c.handle_code 
        except AttributeError:
            # Fallback: recover handle from the PycURL object structure
            # We use offset 16 for 64-bit CPython
            handle_ptr = ctypes.c_void_p.from_address(id(c) + 16).value

        # 3. Explicitly define the C function signature to avoid pointer corruption
        self.libcurl.curl_easy_setopt.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]
        self.libcurl.curl_easy_setopt.restype = ctypes.c_int

        # 4. Apply the setting
        result = self.libcurl.curl_easy_setopt(handle_ptr, CURL_OPT_SSL_EC_CURVES, raw_curve_string)
        print(result)
        print("Selected PQC Mode:", pqc_mode, "| Curve:", raw_curve_string.decode('utf-8'))

        try:
            c.perform()
            
            full_log = "".join(debug_logs)

            # This looks for the pattern: / Cipher / Group / KeyType
            # It captures the text between the second and third forward slash
            match = re.search(r"SSL connection using .*? / .*? / (.*?) /", full_log)

            if match:
                curve = match.group(1).strip()
            else:
                # Fallback: some versions might not have the trailing slash/id-ecPublicKey
                match_alt = re.search(r"SSL connection using .*? / .*? / ([^\s/]+)", full_log)
                curve = match_alt.group(1).strip() if match_alt else "Unknown"

            return Response(
                content=buffer.getvalue(),
                status_code=c.getinfo(pycurl.RESPONSE_CODE),
                headers=header_buffer.getvalue().decode('iso-8859-1'),
                negotiated_curve=curve
            )
        except pycurl.error as e:
            raise ConnectionError(f"PQC Connection Failed: {e}")
        finally:
            c.close()

    def get(self, url, **kwargs): return self.request("GET", url, **kwargs)
    def post(self, url, **kwargs): return self.request("POST", url, **kwargs)
    def put(self, url, **kwargs):    return self.request("PUT", url, **kwargs)
    def patch(self, url, **kwargs):  return self.request("PATCH", url, **kwargs)
    def delete(self, url, **kwargs): return self.request("DELETE", url, **kwargs)

# Global convenience methods
def get(url, **kwargs): return Session().get(url, **kwargs)
def post(url, **kwargs): return Session().post(url, **kwargs)
def put(url, **kwargs):    return Session().put(url, **kwargs)
def patch(url, **kwargs):  return Session().patch(url, **kwargs)
def delete(url, **kwargs): return Session().delete(url, **kwargs)