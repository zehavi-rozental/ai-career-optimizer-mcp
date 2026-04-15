#!/usr/bin/env python3
"""
Final validation before running Streamlit
"""
import sys
import os

print("=" * 60)
print("✅ FINAL VALIDATION - AI Career Optimizer")
print("=" * 60)

# Check 1: Files exist
print("\n📁 Checking files...")
required_files = {
    'app.py': 'Main app',
    'services/google_search.py': 'Google Search',
    'services/ai_service.py': 'AI Service',
    '.streamlit/secrets.toml': 'Secrets',
    '.streamlit/config.toml': 'Config'
}

for file, desc in required_files.items():
    exists = os.path.exists(file)
    status = "✅" if exists else "❌"
    print(f"  {status} {file:40} ({desc})")

# Check 2: Import check
print("\n📦 Checking imports...")
try:
    from services.google_search import GoogleSearchService
    print("  ✅ GoogleSearchService")
except Exception as e:
    print(f"  ❌ GoogleSearchService: {e}")

try:
    from services.ai_service import AIService
    print("  ✅ AIService")
except Exception as e:
    print(f"  ❌ AIService: {e}")

# Check 3: Certifi
print("\n🔐 Checking SSL certificates...")
try:
    import certifi
    print(f"  ✅ Certifi: {certifi.where()[:50]}...")
except Exception as e:
    print(f"  ❌ Certifi: {e}")

# Check 4: Secrets
print("\n🔑 Checking secrets...")
try:
    import toml
    with open('.streamlit/secrets.toml', 'r') as f:
        secrets = toml.load(f)
    
    for key in ['GOOGLE_API_KEY', 'SEARCH_ENGINE_ID', 'GEMINI_API_KEY']:
        val = secrets.get(key, 'MISSING')
        status = "✅" if val and val != 'MISSING' else "⚠️"
        print(f"  {status} {key}")
except Exception as e:
    print(f"  ❌ Error reading secrets: {e}")

print("\n" + "=" * 60)
print("🚀 Ready to run: streamlit run app.py")
print("=" * 60)

