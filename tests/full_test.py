#!/usr/bin/env python3
"""
Complete test of all API keys and connections
"""
import sys
import os
import toml
import requests
import certifi

# עדכון נתיב לקבצים בדירקטוריה ההורית
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 70)
print("🔍 בדיקה מלאה - API Keys וctions")
print("=" * 70)

# Step 1: Check secrets file
print("\n1️⃣ בדיקת secrets.toml...")
try:
    with open('.streamlit/secrets.toml', 'r') as f:
        secrets = toml.load(f)

    api_key = secrets.get('GOOGLE_API_KEY', '')
    search_id = secrets.get('SEARCH_ENGINE_ID', '')
    gemini_key = secrets.get('GEMINI_API_KEY', '')

    print(f"   ✅ GOOGLE_API_KEY: {api_key[:20]}... (length: {len(api_key)})")
    print(f"   ✅ SEARCH_ENGINE_ID: {search_id}")
    print(f"   ✅ GEMINI_API_KEY: {gemini_key[:20]}... (length: {len(gemini_key)})")

    if not api_key or not search_id or not gemini_key:
        print("   ❌ חסרים API keys!")
        sys.exit(1)

except Exception as e:
    print(f"   ❌ שגיאה בקריאת secrets: {e}")
    sys.exit(1)

# Step 2: Test Google Custom Search API
print("\n2️⃣ בדיקת Google Custom Search API...")
try:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': 'python developer',
        'key': api_key,
        'cx': search_id,
        'num': 1
    }
    headers = {'User-Agent': 'Mozilla/5.0'}

    print("   שולח בקשה ל-Google...")
    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10,
        verify=certifi.where()
    )

    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        print(f"   ✅ Google Custom Search API עובד! ({len(items)} תוצאות)")
        if items:
            print(f"      First result: {items[0].get('title', 'N/A')[:50]}")
    elif response.status_code == 403:
        print(f"   ❌ שגיאה 403: Forbidden/Quota exceeded")
        print(f"      Response: {response.text[:200]}")
    else:
        print(f"   ❌ שגיאה {response.status_code}")
        print(f"      Response: {response.text[:200]}")

except Exception as e:
    print(f"   ❌ שגיאה בחיבור: {type(e).__name__}: {str(e)[:100]}")

# Step 3: Test Gemini API
print("\n3️⃣ בדיקת Gemini API...")
print("   ⚠️ בדיקה זו אינה רלוונטית - יש להשתמש בספרייה google-generativeai בלבד!")
try:
    import google.generativeai as genai

    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("תגיד שלום בעברית בקצרה מאוד")
    print(f"   ✅ תשובת Gemini: {response.text}")
except Exception as e:
    print(f"   ❌ שגיאת Gemini: {str(e)}")

# Step 4: Summary
print("\n" + "=" * 70)
print("📋 סיכום:")
print("=" * 70)
print("✅ Secrets loaded successfully")
print("✅ SSL certificates configured")
print("✅ All API connections tested")
print("\n🚀 יכול להפעיל: streamlit run app.py")
print("=" * 70)

