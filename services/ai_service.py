import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # ניקוי מוחלט של מפתח ה-API
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")
        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None
        try:
            genai.configure(api_key=api_key)
            # שם המודל המדויק (ללא קידומת models/)
            model = genai.GenerativeModel('gemini-1.5-flash')

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
            6. עטוף מילים לשיפור ב-<span style='color:#2ecc71; font-weight:bold;'>word</span>.
            """

            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"שגיאת AI: {str(e)}")
            return None