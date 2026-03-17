import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # שליפת המפתח מה-Secrets
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        # הגדרה רשמית - פותר את שגיאות ה-400/404 שראינו
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        בתור מומחה גיוס, נתח את רמת ההתאמה:

        קורות חיים: {resume_text[:3000]}
        תיאור משרה: {job_description[:2000]}

        אנא השב בעברית בצורה הבאה:
        - ציון התאמה כללי (0-100)
        - פירוט נקודות חוזק (למה זה מתאים)
        - פערים מרכזיים (מה חסר)
        - 3 טיפים קונקרטיים לשיפור קורות החיים למשרה זו
        """

        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return None