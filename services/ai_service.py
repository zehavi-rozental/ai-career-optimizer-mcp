import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def get_available_model():
        """בדוק קודם לקוד איזה מודל זמין, כדי למנוע שגיאת 404"""
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")
        if not api_key:
            return None

        genai.configure(api_key=api_key)
        models_to_try = ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.5-pro']

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # בדיקה מהירה אם המודל עובד
                test_response = model.generate_content("test", generation_config=genai.types.GenerationConfig(max_output_tokens=10))
                if test_response:
                    return model_name
            except:
                continue

        return 'gemini-pro'  # ברירת מחדל אם כל דבר נכשל

    @staticmethod
    def analyze_job_match(resume_text, job_description):
        """ניתוח התאמה עמוק בין קורות חיים למשרה"""
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")
        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None
        try:
            genai.configure(api_key=api_key)

            # בדוק איזה מודל זמין
            available_model = AIService.get_available_model()
            if not available_model:
                st.error("לא ניתן למצוא מודל זמין")
                return None

            model = genai.GenerativeModel(available_model)

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