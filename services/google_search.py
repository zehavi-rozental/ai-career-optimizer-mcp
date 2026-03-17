import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        # שליפה נקייה מה-Secrets
        api_key = st.secrets.get("GOOGLE_API_KEY", "").strip().replace('"', '')
        search_id = st.secrets.get("SEARCH_ENGINE_ID", "").strip().replace('"', '')

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_id,
            'q': query,
            'num': 5  # נבקש פחות תוצאות כדי לוודא שזה עובר
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                # זה ידפיס לך בדיוק מה הבעיה עכשיו
                error_info = response.json().get('error', {}).get('message', 'שגיאה לא ידועה')
                st.error(f"גוגל אומר: {error_info}")
                return []

            return response.json().get('items', [])
        except Exception as e:
            st.error(f"שגיאת תקשורת: {e}")
            return []