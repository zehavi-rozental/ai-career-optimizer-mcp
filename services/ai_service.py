import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")
        if not api_key:
            st.error("Missing Gemini API Key")
            return None

        try:
            genai.configure(api_key=api_key)

            # מציאת המודל הזמין ביותר בחשבון שלך באופן אוטומטי
            available_models = [m.name for m in genai.list_models() if
                                'generateContent' in m.supported_generation_methods]

            # עדיפות ל-1.5 פלאש, אחר כך פרו, ואז מה שיש
            selected_model = None
            for model_name in ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.0-pro']:
                if model_name in available_models:
                    selected_model = model_name
                    break

            if not selected_model:
                selected_model = available_models[0]  # פתרון אחרון: קח את הראשון שזמין

            model = genai.GenerativeModel(selected_model)

            prompt = f"""
            בתור מומחה גיוס, בצע ניתוח התאמה ארוך ומפורט מאוד (מינימום 3 פסקאות לכל חלק).
            תיאור משרה: {job_description}
            קורות חיים: {resume_text}

            מבנה תשובה:
            SCORE: [מספר]
            ### 📊 ניתוח אסטרטגי מורחב
            ### ✅ נקודות חוזק (מפורט)
            ### ⚠️ פערים
            ### ✍️ המלצות לשיפור (עטפי ביטויים ב- <span style='color:#2ecc71; font-weight:bold;'>ביטוי</span>)
            """

            response = model.generate_content(
                prompt,
                generation_config={"max_output_tokens": 3000, "temperature": 0.7}
            )
            return response.text

        except Exception as e:
            st.error(f"שגיאת מערכת: {str(e)}")
            return None