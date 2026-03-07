import httpx
import json

url = "http://localhost:5000/api/recommend"
payload = {
    "budget": 120000,
    "usage_type": "gamedev_ue5",
    "num_builds": 1
}

try:
    response = httpx.post(url, json=payload, timeout=30.0)
    print(f"Status: {response.status_code}")
    data = response.json()
    if data.get("success"):
        print("Success! Got recommendations for gamedev_ue5.")
        builds = data.get("recommendations", [])
        if builds:
            print(f"Best Build Performance Score: {builds[0].get('performance_score')}")
    else:
        print(f"API Error: {data.get('error')}")
except Exception as e:
    print(f"Request failed: {e}")
