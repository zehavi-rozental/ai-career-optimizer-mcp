import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query):
        api_key = st.secrets.get("GOOGLE_API_KEY", "").strip()
        search_id = st.secrets.get("SEARCH_ENGINE_ID", "").strip()

        url = "https://www.googleapis.com/customsearch/v1"
        params = {'key': api_key, 'cx': search_id, 'q': query}

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                # זה ידפיס לך בדיוק מה גוגל אומר!
                error_detail = response.json().get('error', {}).get('message', 'Unknown Error')
                st.error(f"גוגל מחזיר שגיאה: {error_detail} (קוד: {response.status_code})")
                return []

            items = response.json().get('items', [])
            return items
        except Exception as e:
            st.error(f"שגיאת תקשורת: {e}")
            return []

        # השאילתה המדויקת שתביא לך משרות ולא "מלל"
        # אנחנו מוסיפים מילות מפתח כדי שגוגל יבין שאנחנו מחפשים דפי משרה
        enhanced_query = f"{query} \"תיאור משרה\" OR \"דרושים\""

        # האתרים הממוקדים שלך
        sites = "(site:alljobs.co.il OR site:gotfriends.co.il OR site:jobinfo.co.il OR site:nisha.co.il)"
        full_query = f"{enhanced_query} {sites}"

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_id,
            'q': full_query,
            'num': 5  # נביא את 5 המשרות הכי רלוונטיות
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            # אם עדיין יש 403, זה אומר שגוגל דורש המתנה של כמה דקות לעדכון ה-Key
            if response.status_code == 403:
                st.warning("🔄 גוגל מעדכן את הרשאות המפתח. אנא המתיני דקה ורענני את הדף.")
                return []

            response.raise_for_status()
            data = response.json()
            items = data.get('items', [])

            if not items:
                st.info("לא מצאתי משרות ספציפיות כרגע. נסי לשנות מעט את מילות החיפוש.")
                return []

            return [{
                "title": item.get('title'),
                "link": item.get('link'),
                "snippet": item.get('snippet'),
                "display_link": item.get('displayLink')
            } for item in items]

        except Exception as e:
            st.error(f"שגיאת חיבור: {e}")
            return []