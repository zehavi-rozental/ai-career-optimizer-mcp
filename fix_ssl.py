import ssl
import certifi
import requests

print("Fixing SSL Certificate Issue...")
print(f"CA Bundle location: {certifi.where()}")

# Test with SSL verification disabled (temporary fix)
api_key = "AIzaSyB6IWAc-6ynvTj0ytdySFRMOw0nswCo_z8"
search_id = "d24740ed7e6fb4cd5"
query = "python developer"

url = "https://www.googleapis.com/customsearch/v1"
params = {'q': query, 'key': api_key, 'cx': search_id, 'num': 5}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    # Try with certifi certificates
    print("\nAttempting with certifi certificates...")
    response = requests.get(url, params=params, headers=headers, timeout=15, verify=certifi.where())
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Found {len(data.get('items', []))} results")
        if data.get('items'):
            print(f"First: {data['items'][0].get('title', 'N/A')[:60]}")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"❌ Failed: {e}")

