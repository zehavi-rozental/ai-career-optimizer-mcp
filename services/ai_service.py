import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # ניקוי המפתח
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing API Key")
            return None

        try:
            # הגדרה מפורשת של ה-API
            genai.configure(api_key=api_key)

            # תיקון ה-404: שימוש בשם המודל ללא קידומת models/
            model = genai.GenerativeModel('gemini-1.5-flash')

            # דרישה לניתוח ארוך ומפורט מאוד
            prompt = f"""
            נתח בצורה מקצועית, ארוכה ומפורטת מאוד את ההתאמה. 
            אל תחסוך במילים. ספק הסברים מעמיקים לכל סעיף.

            תיאור משרה: {job_description}
            קורות חיים: {resume_text}

            מבנה התשובה:
            SCORE: [מספר]
            ### 📊 ניתוח התאמה מעמיק
            [כאן כתוב לפחות 3 פסקאות מפורטות]
            ### ✅ נקודות חוזק משמעותיות
            ### ⚠️ פערים שדורשים התייחסות
            ### ✍️ הנחיות מפורטות לשיפור (עטפי ביטויים להוספה ב- <span style='color:#2ecc71; font-weight:bold;'>ביטוי</span>)
            """

            # פתרון לתיאור ארוך: הוספת הגדרות יצירה
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2048,  # מאפשר תשובה ארוכה מאוד
                    temperature=0.7
                )
            )
            return response.text
        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return None