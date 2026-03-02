import sys
sys.path.insert(0, '.')
from services.google_search import GoogleSearchService

print("Testing Google Search API...")
results = GoogleSearchService.search_jobs('python developer')
print(f'Results: {len(results)} jobs found')
if results:
    for i, job in enumerate(results[:3], 1):
        print(f"\n{i}. {job.get('title', 'N/A')[:50]}")
        print(f"   URL: {job.get('link', 'N/A')[:60]}")
else:
    print("No results found")

