import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        # משיכת המפתחות מתוך secrets.toml
        # שימי לב ששמות המשתנים כאן צריכים להיות בדיוק כמו ב-secrets.toml שלך
        api_key = st.secrets.get("GOOGLE_API_KEY")
        search_id = st.secrets.get("SEARCH_ENGINE_ID")

        if not api_key or not search_id:
            st.error("Missing Search API keys in secrets.toml. Please check your configuration.")
            return []

        # הגדרת חיפוש ממוקד באתרים הנבחרים בלבד
        sites = "site:alljobs.co.il OR site:gotfriends.co.il OR site:jobinfo.co.il OR site:nisha.co.il"
        full_query = f"{query} {sites}"

        # בניית ה-URL ל-API של גוגל
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_id}&q={full_query}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # בדיקה שהבקשה עברה בשלום
            items = response.json().get('items', [])

            job_results = []
            for item in items:
                job_results.append({
                    "title": item.get('title'),
                    "link": item.get('link'),
                    "snippet": item.get('snippet'),  # התקציר שיוצג ויועבר לניתוח
                    "display_link": item.get('displayLink')
                })
            return job_results
        except Exception as e:
            st.error(f"שגיאה בחיבור למנוע החיפוש: {e}")
            return []