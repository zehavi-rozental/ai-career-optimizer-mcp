import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # ניקוי מוחלט של המפתח למניעת שגיאות 400/404
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '')

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            genai.configure(api_key=api_key)
            # שימוש בנתיב המלא models/gemini-1.5-flash פותר את שגיאת ה-404
            model = genai.GenerativeModel('models/gemini-1.5-flash')

            prompt = f"""
            נתחי את ההתאמה בין קורות החיים למשרה הבאה:
            קורות חיים: {resume_text[:5000]}
            תיאור משרה: {job_description[:5000]}

            מבנה התשובה:
            1. מדד התאמה (0-100%).
            2. הסבר קצר על רמת ההתאמה.
            3. 3 נקודות חוזק.
            4. 3 פערים מרכזיים.
            5. המלצה לשיפור קורות החיים.
            6. עטוף מילות מפתח ב-<span style='color:#2ecc71; font-weight:bold;'>word</span>.
            7. הוסף SCORE: <מספר> בסוף התשובה.
            """

            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"שגיאת AI: {str(e)}")
            return None