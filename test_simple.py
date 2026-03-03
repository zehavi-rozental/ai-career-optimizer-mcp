import requests
import urllib3

# Disable all SSL warnings
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

# Test without verify
api_key = "AIzaSyB6IWAc-6ynvTj0ytdySFRMOw0nswCo_z8"
search_id = "d24740ed7e6fb4cd5"

url = "https://www.googleapis.com/customsearch/v1"
params = {'q': 'python', 'key': api_key, 'cx': search_id, 'num': 1}

print("Testing with verify=False and no SSL...")
try:
    response = requests.get(url, params=params, timeout=10, verify=False)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ SUCCESS!")
        data = response.json()
        print(f"Items: {len(data.get('items', []))}")
    else:
        print(f"Response: {response.text[:300]}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)[:200]}")

