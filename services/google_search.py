import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        # משיכה נקייה של המפתחות
        api_key = st.secrets.get("GOOGLE_API_KEY", "").replace('"', '').strip()
        search_id = st.secrets.get("SEARCH_ENGINE_ID", "").replace('"', '').strip()

        url = "https://www.googleapis.com/customsearch/v1"
        # אנחנו מוסיפים פרמטר לחיפוש בשפה העברית כדי למנוע שגיאות קידוד
        params = {
            'key': api_key,
            'cx': search_id,
            'q': query,
            'lr': 'lang_iw'
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                error_msg = response.json().get('error', {}).get('message', 'Unknown Error')
                st.error(f"⚠️ גוגל עדיין חוסם: {error_msg}")
                return []

            return response.json().get('items', [])
        except Exception as e:
            st.error(f"❌ שגיאת תקשורת: {e}")
            return []