import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        # ניקוי רווחים נסתרים מהמפתחות
        api_key = st.secrets.get("GOOGLE_API_KEY", "").strip()
        cx = st.secrets.get("SEARCH_ENGINE_ID", "").strip()

        # בדיקה אם המפתחות בכלל קיימים
        if not api_key or not cx:
            st.error("המפתחות חסרים ב-secrets.toml")
            return []

        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}"

        try:
            response = requests.get(url)
            result = response.json()

            if "error" in result:
                # זה ידפיס לנו את ה-Reason המדויק שגוגל שולח
                error_msg = result["error"].get("message", "שגיאה לא ידועה")
                st.error(f"גוגל אומר: {error_msg}")
                return []

            return result.get("items", [])
        except Exception as e:
            st.error(f"שגיאת תקשורת: {e}")
            return []