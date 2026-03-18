import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        api_key = st.secrets.get("SERPER_API_KEY", "").strip()
        url = "https://google.serper.dev/search"

        # שאילתה שמחייבת הופעה של "תיאור משרה" ומסננת דפי בית של אתרים
        enhanced_query = f'"{query}" "תיאור משרה" (site:alljobs.co.il OR site:drushim.co.il OR site:linkedin.com/jobs)'

        payload = {
            "q": enhanced_query,
            "gl": "il",
            "hl": "iw",
            "num": 10,
            "autocorrect": True
        }
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            results = response.json().get('organic', [])
            # סינון תוצאות קצרות מדי שאינן משרות אמיתיות
            return [r for r in results if len(r.get('snippet', '')) > 60]
        except:
            return []
