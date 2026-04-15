import requests
import streamlit as st
import re

class GoogleSearchService:
    @staticmethod
    def calculate_quick_score(resume_text, job_snippet):
        if not resume_text or not job_snippet:
            return 0
        resume_words = set(re.findall(r'\w+', resume_text.lower()))
        job_words = set(re.findall(r'\w+', job_snippet.lower()))
        if not job_words:
            return 0
        common = resume_words.intersection(job_words)
        # חישוב ציון משופר ששומר על רף של 35% לפחות
        score = min(int((len(common) / (len(job_words) + 1)) * 350), 98)
        return max(score, 35)

    @staticmethod
    def search_jobs(query, resume_text="", page=1):
        api_key = st.secrets.get("SERPER_API_KEY", "").strip()
        url = "https://google.serper.dev/search"

        # השאילתה המקורית והחכמה שלך לסינון מקסימלי
        refined_query = (
            f'intitle:"{query}" (intitle:משרה OR intitle:דרוש OR "Apply Now") '
            f'-inurl:search -inurl:results -inurl:jobs-list -inurl:category '
            f'-"265 משרות" -"משרות חמות" -"רשימת משרות"'
        )

        payload = {
            "q": refined_query,
            "gl": "il",
            "hl": "iw",
            "num": 15,
            "page": page
        }
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            results = response.json().get('organic', [])
            filtered_jobs = []

            for res in results:
                title = res.get('title', '')
                snippet = res.get('snippet', '')
                link = res.get('link', '').lower()

                # סינון אתרי אינדקס כפי שהגדרת במקור
                if bool(re.search(r'\d{2,}', title)) or any(word in title for word in ["תוצאות", "חיפוש", "לוח"]):
                    continue
                if any(x in link for x in ["/search", "/results", "jobs-list"]):
                    continue

                res['quick_score'] = GoogleSearchService.calculate_quick_score(resume_text, snippet + " " + title)
                filtered_jobs.append(res)

            return filtered_jobs[:10]
        except Exception as e:
            st.error(f"Search Error: {e}")
            return []

    @staticmethod
    def get_full_job_content(url):
        # המפתח מהתמונה שלך
        api_key = st.secrets.get("SERPER_API_KEY", "").strip()
        scrape_url = "https://google.serper.dev/scrape"
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        # autofill=True שולף את תיאור המשרה בצורה נקייה
        payload = {"url": url, "autofill": True}

        try:
            response = requests.post(scrape_url, headers=headers, json=payload, timeout=10)
            data = response.json()
            # שליפת התוכן המזוקק
            return data.get('metadata', {}).get('description', data.get('text', ""))
        except:
            return ""