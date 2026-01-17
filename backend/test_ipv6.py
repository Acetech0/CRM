import requests
import sys

try:
    print("Testing connection to http://[::1]:8000/api/v1/websites/...")
    # Attempt a GET request to ipv6 localhost
    resp = requests.options("http://[::1]:8000/api/v1/websites/")
    print(f"IPv6 Status: {resp.status_code}")
except Exception as e:
    print(f"IPv6 Connection Failed: {e}")
