import requests
import streamlit as st


class GoogleSearchService:
    @staticmethod
    def search_jobs(query, page=1):
        """חיפוש משרות ממוקד עם סינון דפי תוצאות כלליים"""
        api_key = st.secrets.get("SERPER_API_KEY", "").strip()
        url = "https://google.serper.dev/search"

        # שאילתה שמחפשת משרות ספציפיות ומונעת דפי אינדקס
        enhanced_query = f'"{query}" "תיאור משרה" -inurl:search -inurl:results'

        payload = {
            "q": enhanced_query,
            "gl": "il",  # חיפוש בישראל
            "hl": "iw",  # שפה עברית
            "num": 10,
            "page": page
        }
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            results = response.json().get('organic', [])

            # סינון ידני של תוצאות שנראות כמו "מצאנו X משרות"
            filtered_jobs = []
            for res in results:
                title = res.get('title', '')
                if "נמצאו" not in title and "הצעות עבודה" not in title:
                    filtered_jobs.append(res)
            return filtered_jobs
        except Exception as e:
            st.error(f"Search Error: {e}")
            return []

    @staticmethod
    def get_full_job_content(url):
        """שימוש ב-Serper Scrape כדי להביא את כל הטקסט של המשרה מהאתר"""
        api_key = st.secrets.get("SERPER_API_KEY", "").strip()
        scrape_url = "https://google.serper.dev/scrape"

        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        payload = {"url": url}

        try:
            # שליחת בקשה לשאיבת המלל המלא מהדף
            response = requests.post(scrape_url, headers=headers, json=payload, timeout=20)
            data = response.json()

            # החזרת הטקסט המלא שנמצא בדף
            full_text = data.get('text', "")

            if len(full_text) < 100:
                return "לא ניתן היה לשאוב תיאור מלא באופן אוטומטי. מומלץ להעתיק ידנית מהאתר."

            return full_text
        except Exception as e:
            return f"שגיאה בשאיבת הנתונים: {str(e)}. השתמשי בתיאור הקצר."