import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # שליפת המפתח וניקוי שאריות תווים
        api_key = st.secrets.get("GEMINI_API_KEY", "").replace('"', '').strip()

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            # הגדרת המפתח בספרייה הרשמית
            genai.configure(api_key=api_key)

            # שימוש בנתיב המלא - זה פותר את שגיאת ה-404
            model = genai.GenerativeModel('models/gemini-1.5-flash')

            prompt = f"""
            בתור מומחה גיוס, נתח את רמת ההתאמה בין קורות החיים למשרה.
            השב בעברית מקצועית:

            קורות חיים: {resume_text[:3000]}
            תיאור משרה: {job_description[:2000]}

            מבנה התשובה:
            1. ציון התאמה (0-100%).
            2. הסבר קצר על ההתאמה.
            3. נקודות חוזק ופערים.
            4. המלצה לשיפור קורות החיים.
            """

            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            st.error(f"שגיאת AI: {str(e)}")
            return None