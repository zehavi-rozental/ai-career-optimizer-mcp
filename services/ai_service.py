import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def get_best_model():
        """מזהה דינמית את המודל הכי טוב שזמין בחשבון שלך"""
        try:
            # משיכת רשימת המודלים שגוגל מאשרת לך להשתמש בהם
            available_models = [m.name for m in genai.list_models() if
                                'generateContent' in m.supported_generation_methods]

            # עדיפות 1: Flash (מהיר וחדש)
            for m in available_models:
                if 'gemini-1.5-flash' in m:
                    return m

            # עדיפות 2: Pro (יציב)
            for m in available_models:
                if 'gemini-pro' in m:
                    return m

            # אם לא מצאנו כלום, נחזיר את הראשון ברשימה
            return available_models[0] if available_models else 'gemini-pro'
        except Exception:
            # גיבוי במקרה של תקלה בתקשורת
            return 'gemini-pro'

    @staticmethod
    def analyze_job_match(resume_text, job_description):
        """ניתוח התאמה מפורט עם זיהוי מודל אוטומטי"""
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            genai.configure(api_key=api_key)

            # זיהוי המודל בצורה דינמית מהרשימה של גוגל
            model_name = AIService.get_best_model()
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