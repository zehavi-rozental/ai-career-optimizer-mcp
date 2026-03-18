import google.generativeai as genai
import streamlit as st
import time


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")
        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        genai.configure(api_key=api_key)

        # רשימת מודלים אפשריים לפי סדר עדיפות - זה ימנע את ה-404
        models_to_try = [
            'gemini-1.5-flash',
            'models/gemini-1.5-flash',
            'gemini-pro',
            'models/gemini-pro'
        ]

        prompt = f"""
        בתור מומחה גיוס, בצע ניתוח התאמה מעמיק בעברית.
        SCORE: [מספר בין 0-100]
        ניתוח: {job_description} | {resume_text}
        סמן מילים להוספה בירוק: <span style='color:#2ecc71; font-weight:bold;'>מילה</span>
        """

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                error_msg = str(e)
                # אם הבעיה היא מכסה (429), נחכה קצת וננסה שוב
                if "429" in error_msg:
                    st.warning("⚠️ מכסה מלאה, ממתין 10 שניות...")
                    time.sleep(10)
                    continue
                    # אם הבעיה היא שם מודל (404), פשוט נעבור למודל הבא ברשימה
                elif "404" in error_msg:
                    continue
                else:
                    continue

        st.error("❌ לא הצלחנו להתחבר לאף מודל AI. נסה שוב בעוד דקה.")
        return None