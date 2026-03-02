import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        search_id = st.secrets.get("SEARCH_ENGINE_ID")

        if not api_key or not search_id:
            st.error("❌ API keys not configured. Please update .streamlit/secrets.toml with GOOGLE_API_KEY and SEARCH_ENGINE_ID")
            return []

        if not query:
            return []

        url = "https://www.googleapis.com/customsearch/v1"
        params = {'q': query, 'key': api_key, 'cx': search_id, 'num': 5}

        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                return response.json().get('items', [])
            return []
        except Exception:
            return []