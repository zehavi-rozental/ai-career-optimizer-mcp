import sys
sys.path.insert(0, '.')
import toml

# Load secrets
with open('.streamlit/secrets.toml', 'r') as f:
    secrets = toml.load(f)

print("Secrets loaded:")
print(f"  GOOGLE_API_KEY: {secrets.get('GOOGLE_API_KEY', 'MISSING')[:10]}...")
print(f"  SEARCH_ENGINE_ID: {secrets.get('SEARCH_ENGINE_ID', 'MISSING')}")
print(f"  GEMINI_API_KEY: {secrets.get('GEMINI_API_KEY', 'MISSING')[:10]}...")

# Test API directly with requests
import requests

api_key = secrets.get('GOOGLE_API_KEY')
search_id = secrets.get('SEARCH_ENGINE_ID')
query = "python developer"

print(f"\nTesting API with:")
print(f"  Key: {api_key[:20]}...")
print(f"  CX: {search_id}")
print(f"  Query: {query}")

url = "https://www.googleapis.com/customsearch/v1"
params = {'q': query, 'key': api_key, 'cx': search_id, 'num': 5}

try:
    print("\nMaking request...")
    response = requests.get(url, params=params, timeout=15)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Found {len(data.get('items', []))} results")
        if data.get('items'):
            print(f"First: {data['items'][0].get('title', 'N/A')[:50]}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text[:300]}")
except Exception as e:
    print(f"❌ Exception: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()

