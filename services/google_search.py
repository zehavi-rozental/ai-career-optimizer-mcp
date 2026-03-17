import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        # שליפת המפתח החדש מה-Secrets
        api_key = st.secrets.get("SERPER_API_KEY", "").strip().replace('"', '')

        if not api_key:
            st.error("שגיאה: מפתח SERPER_API_KEY חסר ב-Secrets של Streamlit.")
            return []

        url = "https://google.serper.dev/search"

        # בניית שאילתה חכמה שמחפשת רק באתרים הישראליים המובילים
        # ומוודאת שהתוצאות מהזמן האחרון
        search_query = f"{query} (site:alljobs.co.il OR site:jobinfo.co.il OR site:nisha.co.il OR site:gotfriends.co.il)"

        payload = {
            "q": search_query,
            "gl": "il",  # תוצאות מישראל
            "hl": "iw",  # שפה עברית
            "num": 10  # מספר תוצאות
        }

        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)

            if response.status_code == 200:
                results = response.json().get('organic', [])
                # המרה למבנה שהאפליקציה שלך מצפה לו
                formatted_results = []
                for r in results:
                    formatted_results.append({
                        'title': r.get('title', 'ללא כותרת'),
                        'link': r.get('link', '#'),
                        'snippet': r.get('snippet', 'אין תיאור זמין')
                    })
                return formatted_results
            else:
                st.error(f"שגיאת תקשורת עם Serper (קוד: {response.status_code})")
                return []

        except Exception as e:
            st.error(f"שגיאה בביצוע החיפוש: {e}")
            return []