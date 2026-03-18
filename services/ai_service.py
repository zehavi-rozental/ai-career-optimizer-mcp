import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        """גרסה יציבה ללא בדיקות מקדימות למניעת שגיאות 404"""
        # ניקוי המפתח
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            genai.configure(api_key=api_key)

            # חזרה להגדרה הישירה והפשוטה שעבדה
            # השרת שלך כרגע מקבל את השמות האלו ללא הקידומת models/ בגרסה היציבה
            model = genai.GenerativeModel('gemini-1.5-flash')

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
            # אם gemini-1.5-flash נכשל, ניסיון אחרון עם gemini-pro הסטנדרטי
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                return response.text
            except:
                st.error(f"AI Error: {str(e)}")
                return None