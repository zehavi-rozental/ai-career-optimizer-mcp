import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # ניקוי המפתח - קריטי למניעת שגיאת 400
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("מפתח API חסר בהגדרות (Secrets)")
            return None

        try:
            genai.configure(api_key=api_key)

            # הפתרון הסופי ל-404: שימוש בפרמטר model_name עם השם המדויק
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')

            prompt = f"""
            בתור מומחה גיוס טכנולוגי, נתחי את ההתאמה בין קורות החיים למשרה.
            חשוב מאוד: בפרק המלצות לשיפור, עטפי כל ביטוי או מילה שמומלץ להוסיף בתגית הבאה:
            <span style='color:#2ecc71; font-weight:bold;'>ביטוי</span>

            תיאור המשרה המלא: {job_description[:5000]}
            קורות החיים: {resume_text[:4000]}

            השיבי בעברית במבנה הבא:
            SCORE: [מספר בין 0-100 בלבד]
            ### 📊 מדד התאמה
            [הסבר קצר]
            ### ✅ נקודות חוזק
            ### ⚠️ פערים מרכזיים
            ### ✍️ המלצות לשיפור (השתמשי בצבע ירוק לביטויים להוספה)
            """

            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"שגיאת AI: {str(e)}")
            return None