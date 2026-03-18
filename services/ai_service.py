import google.generativeai as genai
import streamlit as st
import time


class AIService:
    @staticmethod
    def get_dynamic_model():
        """מזהה דינמית את המודל הכי טוב שזמין בחשבון שלך"""
        try:
            # משיכת רשימת המודלים המלאה שגוגל מאשרת לך
            available_models = [m.name for m in genai.list_models() if
                                'generateContent' in m.supported_generation_methods]

            # הדפסה ללוג של Streamlit (בשבילנו, לראות מה גוגל מחזיר)
            print(f"Available models: {available_models}")

            # חיפוש מודל Flash 1.5 (הכי טוב לניתוח ארוך)
            for m in available_models:
                if 'gemini-1.5-flash' in m:
                    return m

            # חיפוש מודל Pro (יציב מאוד)
            for m in available_models:
                if 'gemini-pro' in m:
                    return m

            # אם לא נמצא כלום, נחזיר את הראשון שגוגל נותן לנו
            return available_models[0] if available_models else 'models/gemini-1.5-flash'
        except Exception as e:
            print(f"Error listing models: {e}")
            return 'models/gemini-1.5-flash'

    @staticmethod
    def analyze_job_match(resume_text, job_description):
        """ניתוח התאמה מפורט עם בחירת מודל חכמה"""
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            genai.configure(api_key=api_key)

            # זיהוי דינמי של המודל
            model_name = AIService.get_dynamic_model()
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

            # ניסיון שליחה עם טיפול בשגיאת עומס (429)
            try:
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ עומס זמני על השרת, ממתין 5 שניות לניסיון חוזר...")
                    time.sleep(5)
                    return model.generate_content(prompt).text
                raise e

        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return None