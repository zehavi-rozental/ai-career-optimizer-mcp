import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # שליפת המפתח וניקוי תווים מיותרים
        api_key = st.secrets.get("GEMINI_API_KEY", "").replace('"', '').strip()

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            # הגדרת המפתח
            genai.configure(api_key=api_key)

            # יצירת המודל - שימי לב לשם המדויק כאן שפותר את ה-404
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            אנא נתח את רמת ההתאמה בין קורות החיים למשרה הבאה.
            השב בעברית מקצועית:

            קורות חיים:
            {resume_text[:3000]}

            תיאור משרה:
            {job_description[:2000]}

            מבנה התשובה:
            1. ציון התאמה (0-100%).
            2. הסבר קצר על ההתאמה.
            3. 3 נקודות חוזק.
            4. 3 פערים מרכזיים.
            5. המלצה לשיפור קורות החיים.
            """

            # שליחת הבקשה בצורה שתואמת לגרסאות החדשות
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            # כאן אנחנו תופסים את שגיאת ה-404 ומציגים אותה בצורה ברורה
            st.error(f"שגיאת AI (404/400): {str(e)}")
            return None