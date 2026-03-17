import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # שליפת המפתח וניקוי מוחלט
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-1.5-flash')

            # פרומפט משופר עם הנחיית צביעה בירוק
            prompt = f"""
            בתור מומחה גיוס טכנולוגי בכיר, נתח את ההתאמה בין קורות החיים למשרה הבאה.

            הנחיות חשובות:
            1. בפרק "המלצות לשיפור", עטוף מילים או ביטויים שמומלץ להוסיף לקורות החיים בתגית: <span style='color:#2ecc71; font-weight:bold;'>ביטוי</span>.
            2. החזר ציון התאמה מספרי בלבד בשורה הראשונה.

            תיאור המשרה:
            {job_description[:5000]}

            קורות חיים:
            {resume_text[:4000]}

            מבנה התשובה הנדרש בעברית:
            SCORE: [כאן הציון מ-0 עד 100]

            ### 📊 מדד התאמה
            [הסבר קצר על הציון]

            ### ✅ נקודות חוזק מרכזיות
            - [נקודה 1]

            ### ⚠️ פערים שצריך לגשר עליהם
            - [פער 1]

            ### ✍️ המלצות לשיפור קורות החיים (בצבע ירוק)
            [כאן הטקסט עם הביטויים הירוקים שמומלץ להוסיף]
            """

            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return None