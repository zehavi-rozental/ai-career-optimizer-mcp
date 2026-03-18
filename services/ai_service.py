import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # ניקוי מוחלט של המפתח למניעת שגיאות 400
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            genai.configure(api_key=api_key)

            # השינוי הגאוני: מעבר ל-gemini-pro ללא קידומת models/
            # זה המודל הכי יציב שיפתור את שגיאת ה-404
            model = genai.GenerativeModel('gemini-pro')

            # פרומפט משופר לניתוח ארוך מאוד (3000 טוקנים)
            prompt = f"""
            בתור מומחה גיוס טכנולוגי בכיר, בצעי ניתוח התאמה ארוך, מעמיק ומפורט ביותר.
            אל תסתפקי בנקודות קצרות - הסבירי כל סעיף בפירוט רב (מינימום 2-3 פסקאות לכל פרק).

            תיאור המשרה המלא: {job_description}
            קורות החיים: {resume_text}

            מבנה התשובה הנדרש (בעברית):
            SCORE: [מספר בין 0 ל-100 בלבד]

            ### 📊 ניתוח התאמה אסטרטגי ומפורט
            [כאן כתבי הסבר ארוך ומפורט על הקשר בין הניסיון למשרה]

            ### ✅ נקודות חוזק מרכזיות (בהרחבה)
            [פירוט מעמיק של לפחות 3 נקודות והסבר למה הן קריטיות למעסיק]

            ### ⚠️ פערים וחסמים שדורשים התייחסות
            [פירוט של מה חסר ואיך זה משפיע על המועמדות]

            ### ✍️ המלצות מעשיות לשיפור קורות החיים (בירוק)
            חשוב: עטפי כל ביטוי או מילה טכנית שמומלץ להוסיף בתגית הבאה כדי שיוצגו בירוק:
            <span style='color:#2ecc71; font-weight:bold;'>הביטוי להוספה</span>
            """

            # הגדרות ליצירת טקסט עשיר ומפורט
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=3000,
                    temperature=0.8
                )
            )
            return response.text

        except Exception as e:
            # אם גם זה נכשל, נציג את השגיאה המדויקת לתיקון
            st.error(f"AI Error: {str(e)}")
            return None