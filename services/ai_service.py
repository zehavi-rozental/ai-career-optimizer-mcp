import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def get_available_model():
        """זיהוי דינמי של המודל - מה שעבד בקומיט העליון"""
        try:
            # רשימת מודלים לניסיון בסדר עדיפות
            models_to_try = ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-1.5-flash', 'models/gemini-pro']

            for m_name in models_to_try:
                try:
                    m = genai.GenerativeModel(m_name)
                    # בדיקה מינימלית אם המודל מגיב
                    m.generate_content("hi", generation_config={"max_output_tokens": 1})
                    return m_name
                except:
                    continue
            return 'gemini-1.5-flash'  # ברירת מחדל אחרונה
        except:
            return 'gemini-1.5-flash'

    @staticmethod
    def analyze_job_match(resume_text, job_description):
        """ניתוח התאמה מפורט - מבוסס על הקומיט bd1727c"""
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            genai.configure(api_key=api_key)

            # בחירת מודל דינמית כפי שהיה בקומיט bd1727c
            model_name = AIService.get_available_model()
            model = genai.GenerativeModel(model_name)

            prompt = f"""
            בתור מומחה גיוס בכיר, בצע ניתוח התאמה ארוך, מפורט ומעמיק ביותר בין קורות החיים למשרה.
            אל תכתוב בנקודות קצרות בלבד - הרחב והסבר כל סעיף במינימום 2-3 פסקאות.

            תיאור המשרה המלא: {job_description}
            קורות החיים: {resume_text}

            מבנה התשובה הנדרש (השיבי בעברית):
            SCORE: [מספר בין 0-100 בלבד]

            ### 📊 ניתוח התאמה אסטרטגי ומפורט
            [כאן כתבי הסבר ארוך ומעמיק על הקשר בין הניסיון למשרה]

            ### ✅ נקודות חוזק מרכזיות (בהרחבה)
            [פירוט של לפחות 3 נקודות חוזק והסבר למה הן קריטיות למעסיק]

            ### ⚠️ פערים וחסמים שדורשים התייחסות
            [פירוט של מה חסר ואיך זה משפיע על המועמדות]

            ### ✍️ המלצות מעשיות לשיפור קורות החיים (בירוק)
            חשוב מאוד: עטוף כל ביטוי או מילה טכנית שמומלץ להוסיף בתגית הבאה כדי שיוצגו בירוק:
            <span style='color:#2ecc71; font-weight:bold;'>הביטוי להוספה</span>
            """

            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=3000,
                    temperature=0.8
                )
            )
            return response.text

        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return None