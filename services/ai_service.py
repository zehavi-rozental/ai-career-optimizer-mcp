import google.generativeai as genai
import streamlit as st
import time


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # 1. ניקוי אגרסיבי של המפתח - מוודא שאין שאריות תווים
        raw_key = st.secrets.get("GEMINI_API_KEY", "")
        api_key = "".join(raw_key.split()).replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        genai.configure(api_key=api_key)

        # 2. רשימת התאבדות - כל השמות האפשריים שגוגל מקבל ב-v1beta
        # הוספתי שמות ספציפיים שראינו שעבדו בהיסטוריית הקומיטים שלך
        models_to_try = [
            'gemini-1.5-flash',
            'models/gemini-1.5-flash',
            'gemini-1.5-flash-latest',
            'gemini-pro',
            'models/gemini-pro'
        ]

        prompt = f"""
        בצע ניתוח התאמה מעמיק בעברית בין קורות החיים למשרה.
        SCORE: [0-100]
        ניתוח מפורט: {job_description[:2000]} | {resume_text[:2000]}
        סמן המלצות בירוק: <span style='color:#2ecc71; font-weight:bold;'>ביטוי</span>
        """

        # 3. ניסיון תקיפה רב-שכבתי
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # בדיקה מהירה אם המודל מגיב בכלל
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                err = str(e).lower()
                # אם חסום (Quota), נחכה וננסה שוב באותו מודל פעם אחת
                if "429" in err:
                    st.warning(f"⚠️ עומס במודל {model_name}, מנסה שוב...")
                    time.sleep(2)
                    try:
                        return model.generate_content(prompt).text
                    except:
                        continue
                # אם לא נמצא (404), פשוט עוברים למודל הבא ברשימה
                continue

        # 4. מוצא אחרון - ניסיון דינמי אם כל השאר נכשלו
        try:
            available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available:
                model = genai.GenerativeModel(available[0])
                return model.generate_content(prompt).text
        except:
            pass

        st.error("❌ גוגל חוסם את הבקשות כרגע (שגיאה 429/404). המתן 2 דקות ונסה שוב.")
        return None