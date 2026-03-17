import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        api_key = st.secrets.get("SERPER_API_KEY", "").strip()
        url = "https://google.serper.dev/search"

        # שאילתה "גאונית" שמסננת דפי אינדקס ריקים ומחפשת תיאור מלא
        enhanced_query = f'"{query}" משרה מלאה (AllJobs OR Jobinfo OR LinkedIn) "תיאור משרה"'

        payload = {"q": enhanced_query, "gl": "il", "hl": "iw", "num": 10}
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        response = requests.post(url, headers=headers, json=payload)
        results = response.json().get('organic', [])

        # סינון: רק תוצאות שיש להן תוכן משמעותי
        valid_results = [r for r in results if len(r.get('snippet', '')) > 50]
        return valid_results
