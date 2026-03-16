import streamlit as st
import os
import json
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from utils.docx_generator import create_improved_docx

# הגדרות דף - חייב להיות הפקודה הראשונה של streamlit
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# אתחול Session State לשמירת נתונים בין הרצות
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "search_results" not in st.session_state: st.session_state.search_results = []
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None

st.title("🎯 AI Career Optimizer Pro")

# --- שלב 1: סרגל צדי להעלאת קורות חיים ---
with st.sidebar:
    st.header("📄 שלב 1: העלאת קורות חיים")
    pdf_file = st.file_uploader("העלי קובץ PDF של קורות החיים שלך", type=['pdf'])

    if pdf_file:
        with st.spinner("מחלץ טקסט מה-PDF..."):
            extracted_text = extract_text_from_pdf(pdf_file)
            if extracted_text:
                st.session_state.cv_text = extracted_text
                st.success("✅ קורות החיים נטענו בהצלחה!")
            else:
                st.error("לא הצלחנו לקרוא את הקובץ. ודאי שהוא לא מוגן בסיסמה.")

# --- שלב 2: לוח משרות חכם ---
st.subheader("🔍 שלב 2: לוח משרות חכם")
query = st.text_input("איזה תפקיד את מחפשת?", placeholder="למשל: Full Stack Developer, Data Analyst...")

if st.button("חפש משרות", type="primary"):
    if query:
        with st.spinner(f"מחפש משרות עבור {query}..."):
            st.session_state.search_results = GoogleSearchService.search_jobs(query)
    else:
        st.error("נא להזין שם תפקיד לחיפוש")

if st.session_state.search_results:
    st.write("### בחרי לוח משרות לצפייה:")
    cols = st.columns(3)
    for i, item in enumerate(st.session_state.search_results):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"#### {item['source']}")
                st.write(item.get('desc', 'צפי במשרות עדכניות בלוח זה'))
                st.link_button(f"פתח משרות ב-{item['source']} 🚀", item['link'])

st.divider()

# --- שלב 3: ניתוח והתאמה ---
st.subheader("📊 שלב 3: ניתוח התאמה ושיפור קורות חיים")
st.info("לאחר שמצאת משרה מעניינת, העתיקי את תיאור המשרה (Job Description) והדביקי כאן:")

job_input = st.text_area("תיאור המשרה:", height=200, placeholder="הדביקי כאן את דרישות התפקיד...")

if st.button("🚀 נתח ושפר את קורות החיים שלי", type="primary"):
    if not job_input:
        st.error("נא להדביק את תיאור המשרה!")
    elif not st.session_state.cv_text:
        st.error("נא להעלות קורות חיים בשלב 1 (בצד)")
    else:
        with st.spinner("Gemini מנתח את ההתאמה ומכין הצעות לשיפור..."):
            # פרום (Prompt) ממוקד שמבטיח קבלת JSON תקין
            prompt = f"""
            Analyze the following CV against the Job Description. 
            Respond ONLY with a valid JSON object. No markdown, no backticks.

            Format:
            {{
              "score": (int 0-100),
              "missing_skills": ["skill1", "skill2"],
              "action_plan": "overall strategy",
              "improved_sections": [
                {{"original": "sentence from CV", "improved": "better version for this job", "explanation": "why this change helps"}}
              ]
            }}

            CV Content: {st.session_state.cv_text[:3000]}
            Job Description: {job_input[:3000]}
            """

            res = AIService.get_response(prompt)
            if res:
                st.session_state.analysis_results = res
                st.balloons()

# הצגת תוצאות הניתוח
if st.session_state.analysis_results:
    res = st.session_state.analysis_results

    # תצוגה גרפית של הציון
    col_score, col_skills = st.columns([1, 2])

    with col_score:
        score = res.get('score', 0)
        st.metric("ציון התאמה", f"{score}%")
        if score > 80:
            st.success("התאמה גבוהה מאוד!")
        elif score > 50:
            st.warning("יש פוטנציאל, כדאי לשפר")
        else:
            st.error("התאמה נמוכה - נדרש שינוי משמעותי")

    with col_skills:
        st.write("### 🛠️ כישורים חסרים שכדאי להוסיף:")
        skills = res.get('missing_skills', [])
        if skills:
            for s in skills:
                st.markdown(f"- **{s}**")
        else:
            st.write("נראה שיש לך את כל כישורי הליבה!")

    st.write("### 📝 דו\"ח שיפור קורות חיים (מילה במילה)")
    improved = res.get('improved_sections', [])
    if improved:
        for section in improved:
            with st.expander(f"שיפור בנושא: {section.get('explanation', '')[:50]}..."):
                st.info(f"💡 **הסבר:** {section.get('explanation', '')}")
                st.markdown(f"**❌ המקור:** {section.get('original', '')}")
                st.success(f"**✅ הגרסה המומלצת:** {section.get('improved', '')}")

    st.write("### 💡 תוכנית פעולה כללית")
    st.info(res.get('action_plan', "התמקדי בהדגשת הניסיון הרלוונטי ביותר לדרישות המשרה."))

    # --- שלב 4: הורדת Word ---
    st.divider()
    st.subheader("📥 שלב 4: הורדת קורות חיים משופרים")

    if st.button("צור קובץ Word עם השיפורים"):
        try:
            # יצירת קובץ ה-Word בזיכרון
            docx_data = create_improved_docx(st.session_state.cv_text, res.get('improved_sections', []))

            st.download_button(
                label="לחצי כאן להורדת הקובץ המוכן 📄",
                data=docx_data,
                file_name="Improved_CV_Optimizer.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            st.success("הקובץ נוצר בהצלחה!")
        except Exception as e:
            st.error(f"שגיאה ביצירת הקובץ: {e}")