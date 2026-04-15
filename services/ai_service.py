import streamlit as st
import google.generativeai as genai
import os
import ssl


class AIService:
    @staticmethod
    def _setup_network():
        """הגדרות לעקיפת חסימת SSL בנטפרי"""
        os.environ['PYTHONHTTPSVERIFY'] = '0'
        os.environ['CURL_CA_BUNDLE'] = ''
        os.environ['GOOGLE_API_USE_MTLS'] = 'never'
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
        except:
            pass

    @staticmethod
    def analyze_job_match(resume_text, job_description):
        AIService._setup_network()

        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")
        if not api_key:
            return "❌ חסר מפתח API ב-Secrets"

        try:
            # הגדרה עם transport='rest' כדי למנוע את ה"סיבוב" האינסופי בנטפרי
            genai.configure(api_key=api_key, transport='rest')

            # שלב הגאונות: בודקים איזה מודלים באמת זמינים לך בחשבון
            available_models = [m.name for m in genai.list_models() if
                                'generateContent' in m.supported_generation_methods]

            if not available_models:
                return "❌ גוגל טוענת שאין מודלים זמינים למפתח הזה. בדקי אם ה-API Key פעיל."

            # בחירת המודל הכי טוב ממה שיש (מחפשים flash, אם אין לוקחים pro)
            selected_model = next((m for m in available_models if "1.5-flash" in m), available_models[0])

            model = genai.GenerativeModel(selected_model)

            prompt = f"נתחי התאמה ב-5 שורות עברית (ציון, חוזקות, פערים):\nקו\"ח: {resume_text[:1000]}\nמשרה: {job_description[:1000]}"

            response = model.generate_content(prompt, request_options={"timeout": 20})

            if response and response.text:
                return response.text
            return "❌ התקבלה תשובה ריקה מגוגל."

        except Exception as e:
            return f"❌ שגיאה סופית: {str(e)[:150]}"

    @staticmethod
    def clean_scraped_text(scraped_text, original_snippet):
        return scraped_text[:1500] if scraped_text else original_snippet