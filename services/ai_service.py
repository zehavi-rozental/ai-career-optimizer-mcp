import google.generativeai as genai
import streamlit as st


class AIService:
    @staticmethod
    def analyze_job_match(resume_text, job_description):
        # ניקוי המפתח - קריטי למניעת שגיאת 400
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip().replace('"', '').replace("'", "")

        if not api_key:
            st.error("Missing Gemini API Key in Secrets")
            return None

        try:
            # הגדרת ה-API
            genai.configure(api_key=api_key)

            # הרעיון הגאוני: שימוש ב-model_name מלא ללא הקידומת models/
            # זה מונע את שגיאת ה-404 בגרסת ה-API v1beta
            model = genai.GenerativeModel('gemini-1.5-flash')

            # פרומפט שדורש ניתוח ארוך, עמוק ומפורט מאוד (כפי שביקשת)
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

            # הגדרות ליצירת טקסט ארוך במיוחד
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=3000,  # הגדלתי ל-3000 לתשובה ארוכה מאוד
                    temperature=0.8  # מעט יותר יצירתיות לניתוח מעמיק
                )
            )
            return response.text

        except Exception as e:
            # הדפסת השגיאה המדויקת לדיבגינג
            st.error(f"AI Error: {str(e)}")
            return None