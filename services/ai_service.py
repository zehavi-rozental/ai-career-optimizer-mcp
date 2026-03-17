import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # שליפת המפתח וניקוי גרשיים מיותרים ליתר ביטחון
        api_key = st.secrets.get("GEMINI_API_KEY", "").replace('"', '').strip()

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            # הגדרה רשמית של המפתח
            genai.configure(api_key=api_key)

            # יצירת המודל - הגרסה היציבה ביותר
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            נתחי את ההתאמה בין קורות החיים למשרה הבאה.
            השיבי בעברית רהוטה ומקצועית:

            קורות חיים: {resume_text[:3000]}
            תיאור משרה: {job_description[:2000]}

            מבנה התשובה:
            1. מדד התאמה (0-100%).
            2. הסבר קצר על רמת ההתאמה.
            3. 3 נקודות חוזק בולטות.
            4. 3 פערים מרכזיים.
            5. המלצה לשיפור קורות החיים עבור משרה זו.
            """

            # שליחת הבקשה
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            # טיפול בשגיאת גרסה במידת הצורך
            st.error(f"AI Error: {str(e)}")
            return None