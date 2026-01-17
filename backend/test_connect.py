import requests
import sys

try:
    print("Testing connection to http://localhost:8000/api/v1/websites...")
    # Attempt a POST request (simulating the Create Website call)
    # We expect 401 Unauthorized (if no token) or 422 Validation Error (if empty body)
    # If connection fails, it raises an exception.
    resp = requests.post("http://localhost:8000/api/v1/websites", json={})
    print(f"Response Status: {resp.status_code}")
    print(f"Response Headers: {resp.headers}")
    print("PASS: Backend is reachable.")
except Exception as e:
    print(f"FAIL: Backend is unreachable. Error: {e}")
