import google.generativeai as genai
import streamlit as st
import time


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        """ניתוח התאמה תוך שימוש במודל יציב וטיפול במכסות (Quota)"""
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            genai.configure(api_key=api_key)

            # שימוש במודל יציב שקיים בוודאות בגרסה החינמית
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            בתור מומחה גיוס בכיר, בצע ניתוח התאמה מעמיק בין קורות החיים למשרה.
            SCORE: [מספר בין 0-100]

            תיאור המשרה: {job_description}
            קורות החיים: {resume_text}

            ספקו ניתוח מפורט בעברית הכולל נקודות חוזק, פערים והמלצות לשיפור.
            עטוף מילות מפתח מומלצות ב: <span style='color:#2ecc71; font-weight:bold;'>מילה</span>
            """

            # שליחת הבקשה
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            if "429" in str(e):
                st.warning("⚠️ עומס על השרת (Quota Exceeded). מנסה שוב בעוד 5 שניות...")
                time.sleep(5)
                # ניסיון חוזר אחד
                try:
                    response = model.generate_content(prompt)
                    return response.text
                except:
                    st.error("❌ חרגת ממכסת הבקשות החינמית של גוגל. המתיני דקה ובוצעי ניתוח מחדש.")
            else:
                st.error(f"AI Error: {str(e)}")
            return None