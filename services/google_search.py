import requests
import streamlit as st

class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        api_key = st.secrets.get("SERPER_API_KEY", "").strip().replace('"', '')
        if not api_key:
            return []

        url = "https://google.serper.dev/search"
        search_query = f'"{query}" משרה מלאה (AllJobs OR Jobinfo OR Nisha OR GotFriends)'

        payload = {"q": search_query, "gl": "il", "hl": "iw"}
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json().get('organic', [])
            return []
        except:
            return []