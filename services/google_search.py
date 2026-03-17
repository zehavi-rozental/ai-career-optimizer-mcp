import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        api_key = st.secrets.get("SERPER_API_KEY", "").strip()
        if not api_key:
            st.error("Missing SERPER_API_KEY")
            return []

        url = "https://google.serper.dev/search"

        # שאילתה ממוקדת לאתרים הישראליים עם מילות מפתח של דרושים
        search_query = f'"{query}" (דרוש OR דרושה OR משרה) site:alljobs.co.il OR site:jobinfo.co.il OR site:nisha.co.il OR site:gotfriends.co.il'

        payload = {"q": search_query, "gl": "il", "hl": "iw"}
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                results = response.json().get('organic', [])
                return [{'title': r.get('title'), 'link': r.get('link'), 'snippet': r.get('snippet')} for r in results]
            return []
        except:
            return []