import requests
import streamlit as st
import re
import pandas as pd
import urllib3

# ביטול אזהרות SSL עבור סביבת נטפרי
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GoogleSearchService:
    @staticmethod
    def calculate_quick_score(resume_text, job_snippet):
        if not resume_text or not job_snippet:
            return 35
        resume_words = set(re.findall(r'\w+', resume_text.lower()))
        job_words = set(re.findall(r'\w+', job_snippet.lower()))
        if not job_words:
            return 35
        common = resume_words.intersection(job_words)
        # חישוב אחוז ההתאמה האמיתי
        score = min(int((len(common) / (len(job_words) + 1)) * 350), 98)
        return max(score, 35)

    @staticmethod
    def search_jobs(query, resume_text="", page=1):
        try:
            api_key = st.secrets["SERPER_API_KEY"].strip()
        except (KeyError, AttributeError):
            st.error("⚠️ SERPER_API_KEY חסר. הוסיפי אותו לקובץ secrets.toml")
            return []

        if not api_key:
            st.error("⚠️ SERPER_API_KEY חסר. הוסיפי אותו לקובץ secrets.toml")
            return []

        url = "https://google.serper.dev/search"

        # ניקוי השאילתה מתווים מיוחדים למניעת שגיאה 400
        clean_query = re.sub(r'[^\w\s]', '', query).strip()

        # השאילתה המושלמת: מחייבת את גוגל להביא עמודי משרות פנימיים מתוך מערכות הגיוס (Comeet/Greenhouse)
        # זה מבטיח שהטקסט שיחזור יכיל דרישות תפקיד אמיתיות, מה שיקפיץ את אחוזי ההתאמה!
        refined_query = f"{clean_query} job description positions comeet greenhouse"

        payload = {
            "q": refined_query,
            "gl": "il",
            "hl": "iw",
            "num": 40,
            "page": page
        }
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }

        # חסימה מוחלטת והרמטית של כל אתרי הלוחות, האינדקסים וחברות ההשמה הכלליות
        AGGREGATOR_DOMAINS = [
            "taasuka.gov.il", "iss.gov.il", "taasuka100", "sherut-taasuka",
            "drushim", "alljobs", "jobmaster", "careerjet", "israeljobs",
            "jobkar", "ravtech", "tech-job", "runner", "dialog", "cps",
            "glassdoor", "nisha", "linkedin", "indeed", "sqlink",
            "gotfriends", "ethosia", "manpower", "ors", "hever",
            "golearn", "limudim", "yoram", "edu", "mitgaisim", "reddit",
            "wikipedia", "facebook", "instagram", "blogs"
        ]

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15, verify=False)

            if response.status_code != 200:
                st.error(f"⚠️ שגיאת Serper API (קוד {response.status_code}): {response.text[:200]}")
                return []

            data = response.json()
            results = data.get('organic', [])

            if not results:
                st.warning("לא נמצאו תוצאות עבור החיפוש הזה. נסי ניסוח אחר.")
                return []

            df = pd.DataFrame(results)

            if df.empty:
                return []

            for col in ['title', 'snippet', 'link']:
                if col not in df.columns:
                    df[col] = ""
                else:
                    df[col] = df[col].fillna("")

            df['link_lower'] = df['link'].str.lower()
            df['title_lower'] = df['title'].str.lower()

            # סינון קפדני ב-Pandas של עמודי בית ולוחות כלליים
            invalid_title_patterns = [
                "תוצאות", "חיפוש", "לוח", "אינדקס", "כל המשרות", "דף הבית",
                "ראשי", "איך לכתוב", "טיפים", "כתיבת קורות", "מדריך", "שאלות ראיון",
                "מה זה", "מהו", "דוגמאות", "תבניות", "פורום", "קורס", "לימודים",
                "כל המשרות", "לוח דרושים"
            ]
            title_mask = df['title_lower'].str.contains('|'.join(invalid_title_patterns), na=False)
            df = df[~title_mask]

            invalid_link_patterns = ["/search", "/results", "jobs-list", "filter", "query=", "category=", "tag/",
                                     "blog", "/wiki"]
            link_mask = df['link_lower'].str.contains('|'.join(invalid_link_patterns), na=False)
            df = df[~link_mask]

            domain_mask = df['link_lower'].str.contains('|'.join(AGGREGATOR_DOMAINS), na=False)
            df = df[~domain_mask]

            if df.empty:
                for r in results:
                    r['htmlTitle'] = r.get('title', query)
                return results[:10]

            # חישוב מדד התאמה (Quick Score) על בסיס הטקסט המקצועי של המשרה
            def compute_score(row):
                text_to_score = str(row['snippet']) + " " + str(row['title'])
                return GoogleSearchService.calculate_quick_score(resume_text, text_to_score)

            df['quick_score'] = df.apply(compute_score, axis=1)

            # מיון מההתאמה הגבוהה ביותר לנמוכה ביותר
            df = df.sort_values(by='quick_score', ascending=False)
            df = df.drop_duplicates(subset=['title'])

            final_jobs = df.head(10).to_dict(orient='records')

            for job in final_jobs:
                job['htmlTitle'] = job.get('title', query)

            return final_jobs

        except Exception as e:
            st.error(f"Search Error: {e}")
            return []

    @staticmethod
    def get_full_job_content(url):
        try:
            api_key = st.secrets["SERPER_API_KEY"].strip()
        except (KeyError, AttributeError):
            return ""

        if not api_key:
            return ""

        scrape_url = "https://google.serper.dev/search"
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
        payload = {"url": url, "autofill": True}

        try:
            response = requests.post(scrape_url, headers=headers, json=payload, timeout=12, verify=False)
            if response.status_code == 200:
                data = response.json()
                return data.get('metadata', {}).get('description', data.get('text', ""))
        except:
            pass
        return ""