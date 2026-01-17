import requests

url = "http://localhost:8000/api/v1/websites/"
headers = {
    "Origin": "http://localhost:5173",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "Authorization,Content-Type"
}

try:
    print(f"Testing OPTIONS {url}")
    response = requests.options(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for k, v in response.headers.items():
        if k.lower().startswith("access-control"):
            print(f"{k}: {v}")
    
    if response.status_code == 200 and "Access-Control-Allow-Origin" in response.headers:
        print("\nCORS Status: OK")
    else:
        print("\nCORS Status: FAILED")

except Exception as e:
    print(f"Error: {e}")
