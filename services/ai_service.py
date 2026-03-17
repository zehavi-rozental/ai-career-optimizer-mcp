import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # ניקוי מוחלט של המפתח למניעת שגיאות 400/404
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            genai.configure(api_key=api_key)
            # שימוש בנתיב המלא models/gemini-1.5-flash פותר את שגיאת ה-404
            model = genai.GenerativeModel('models/gemini-1.5-flash')

            prompt = f"""
            בתור מומחה גיוס טכנולוגי, נתח את ההתאמה בין קורות החיים למשרה.
            חשוב: בפרק "המלצות לשיפור", עטוף מילים שמומלץ להוסיף בתגית: <span style='color:#2ecc71; font-weight:bold;'>ביטוי</span>.

            תיאור המשרה המלא: {job_description[:5000]}
            קורות חיים: {resume_text[:4000]}

            השב בעברית במבנה הבא:
            SCORE: [מספר בין 0-100 בלבד]
            ### 📊 מדד התאמה
            [הסבר על הציון]
            ### ✅ נקודות חוזק
            ### ⚠️ פערים
            ### ✍️ המלצות לשיפור (השתמש בצבע ירוק לביטויים להוספה)
            """

            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return None