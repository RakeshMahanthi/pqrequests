A small scaffold for PQC-aware request tooling.

Contents:
- `requests_pqc.py` — the Python package
- `examples/` — small example usage scripts
- `test` - contains sample server to test the implementation 

```
# requests_pqc

Lightweight helpers for making HTTP requests with a focus on experimenting with
post-quantum-capable TLS handshakes. This package is intentionally minimal and
depends on the system `curl` CLI (the current implementation invokes `curl` via
subprocess).

Important: the implementation shipped in `requests_pqc.py` uses the `curl` binary
and parses its verbose output to infer the negotiated KEM/group. Make sure `curl`
is installed and available on PATH. 


Contents
- `requests_pqc.py` — module exposing `request(...)` and convenience helpers
	(`get`, `post`, `put`, `patch`, `delete`). The module returns a `PQCResponse`
	object containing `status_code`, `text`, and `kem_algo` (the parsed negotiated
	KEM/group when available).
- `server.py` — a small dummy HTTP(S) server useful for local testing.
- `examples/` — runnable example scripts demonstrating usage.
- `tests/` — pytest-based integration tests that exercise the library against
	the dummy server.

Requirements
- Python 3.8+
- Curl 8.0+
- OpenSSL 3.5+

Quick install (dev editable install into a venv):

```bash

#From PyPI org
pip install requests_python

# activate your venv first, then from the package root:
python -m pip install -e .
python -m pip install pytest
```


API

Class
- `PQCResponse(status_code, text, kem_algo)` — simple container returned by
	`request(...)`.

Top-level function
- `request(method, url, mode='classical', data=None, headers=None, verify=True, cacert=None, **kwargs)`
	- method: HTTP verb as a string (e.g. 'GET', 'POST')
	- url: target URL
	- mode: one of `classical`, `hybrid`, `pure`. The implementation maps these
		to curl-compatible curve/KEM strings when invoking `curl`.
	- data: request payload (string or object; passed to curl `-d`)
	- headers: dict of headers to send
	- verify: boolean. When False, `-k` is passed to curl to skip TLS verification.
	- cacert: path to CA bundle file. When provided and `verify` is True, the
		curl `--cacert` option will be used to verify the server cert.

Convenience helpers: `get`, `post`, `put`, `patch`, `delete` map to `request`.

Examples

Basic GET (allow self-signed certs):

```python
import requests_pqc

r = requests_pqc.get('https://127.0.0.1:8443/items', verify=False)
print(r.status_code, r.kem_algo)
print(r.text)
```

POST with JSON-like payload and verification disabled:

```python
payload = {'name': 'alice'}
r = requests_pqc.post('https://127.0.0.1:8443/items', data=payload, verify=False)
print(r.status_code, r.kem_algo)
```

Verify using a CA bundle file (positive verification):

```python
r = requests_pqc.get('https://secure.example', verify=True, cacert='/path/to/ca.pem')
```

Notes and limitations
- This implementation shells out to the `curl` CLI and parses verbose stderr
	output to find the negotiated KEM/group. The parsing is brittle and depends on
	the `curl`/OpenSSL versions and their debug message format.
- For production or reliable behavior, consider using a proper HTTP/TLS client
	library (e.g., `requests` + a TLS backend) or a pycurl binding that exposes
	the needed libcurl APIs directly.
- The `mode -> curve` mappings are heuristic. Confirm the strings your local
	curl/OpenSSL accepts.

Testing with the bundled dummy server

1. Start the dummy HTTPS server (it will generate a self-signed cert if none
	 exists):

```bash
python requests_pqc/server.py
```

2. Run the pytest integration tests (they are written to accept the
	 self-signed certs by setting `verify=False` where appropriate):

```bash
python -m pytest -q
```

Contributing
- Feel free to open issues or PRs. If you want more robust TLS handling I
	recommend proposing a pycurl-based or native Python TLS implementation and
	adding tests that cover verification behavior.

License
- MIT (or whatever license you choose — include a LICENSE file if needed)


