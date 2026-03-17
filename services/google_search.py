import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        # שליפה נקייה מה-Secrets (בלי גרשיים מיותרים)
        api_key = st.secrets.get("GOOGLE_API_KEY", "").replace('"', '').strip()
        search_id = st.secrets.get("SEARCH_ENGINE_ID", "").replace('"', '').strip()

        # אם המפתח ריק, לא ננסה אפילו
        if not api_key:
            st.error("המפתח לא הוגדר ב-Secrets")
            return []

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_id,
            'q': query
        }

        try:
            # הוספת פרמטר למניעת Cache (כדי שלא יביא שגיאה ישנה)
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                error_data = response.json().get('error', {})
                # אם המפתח "פג תוקף", נדפיס הוראה ברורה
                if "expired" in error_data.get('message', '').lower():
                    st.error("🔑 המפתח ב-Secrets פג תוקף. אנא הדביקי את המפתח החדש שיצרת הרגע ולחצי Save.")
                else:
                    st.error(f"גוגל מחזיר שגיאה: {error_data.get('message')}")
                return []

            return response.json().get('items', [])
        except Exception as e:
            st.error(f"שגיאת תקשורת: {e}")
            return []