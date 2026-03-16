import streamlit as st
import os
import json
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from utils.docx_generator import create_improved_docx

# הגדרות דף
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# אתחול Session State
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "search_results" not in st.session_state: st.session_state.search_results = []
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None

st.title("🎯 AI Career Optimizer Pro")

# שלב 1: העלאת קורות חיים
with st.sidebar:
    st.header("📄 שלב 1: העלאת קורות חיים")
    pdf_file = st.file_uploader("העלי קובץ PDF", type=['pdf'])
    if pdf_file:
        with st.spinner("מחלץ טקסט מהקובץ..."):
            st.session_state.cv_text = extract_text_from_pdf(pdf_file)
            st.success("✅ קורות החיים נטענו!")

# שלב 2: לוח משרות חכם
st.subheader("🔍 שלב 2: לוח משרות חכם")
query = st.text_input("איזה תפקיד את מחפשת?", placeholder="למשל: Full Stack Developer")

if st.button("חפש משרות", type="primary"):
    if query:
        with st.spinner("מחפש בלוחות המשרות..."):
            st.session_state.search_results = GoogleSearchService.search_jobs(query)
    else:
        st.error("נא להזין תפקיד")

if st.session_state.search_results:
    st.write("### בחרי לוח משרות לצפייה:")
    cols = st.columns(3)
    for i, item in enumerate(st.session_state.search_results):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"#### {item['source']}")
                st.write(item['desc'])
                st.link_button("פתח משרות 🚀", item['link'])

st.divider()

# שלב 3: ניתוח והתאמה
st.subheader("📊 שלב 3: ניתוח התאמה ושיפור קורות חיים")
st.info("לאחר שמצאת משרה מעניינת באחד הלוחות למעלה, העתיקי את תיאור המשרה לכאן:")
job_input = st.text_area("תיאור המשרה (Job Description):", height=150)

if st.button("🚀 נתח ושפר את קורות החיים שלי", type="primary"):
    if not job_input or not st.session_state.cv_text:
        st.error("חסר תיאור משרה או קורות חיים!")
    else:
        with st.spinner("Gemini מנתח וכותב עבורך גרסה משופרת..."):
            prompt = f"""
            Analyze the following CV against the Job Description.
            Return a JSON with:
            1. 'score': int (0-100)
            2. 'missing_skills': list of strings
            3. 'action_plan': string
            4. 'improved_sections': list of objects with 'original', 'improved', 'explanation'.

            CV: {st.session_state.cv_text[:3000]}
            Job Description: {job_input}
            """
            res = AIService.get_response(prompt)
            if res:
                st.session_state.analysis_results = res

if st.session_state.analysis_results:
    res = st.session_state.analysis_results

    col_a, col_b = st.columns([1, 2])
    col_a.metric("ציון התאמה", f"{res.get('score', 0)}%")

    with col_b:
        st.write("### 🛠️ כישורים חסרים")
        for s in res.get('missing_skills', []):
            st.write(f"- {s}")

    st.write("### 📝 דו\"ח שיפור קורות חיים")
    for section in res.get('improved_sections', []):
        with st.expander(f"שיפור סעיף: {section.get('explanation', '')[:50]}..."):
            st.warning(f"**למה זה חשוב?** {section.get('explanation', '')}")
            st.markdown(f"**❌ המקור:** {section.get('original', '')}")
            st.success(f"**✅ הגרסה המשופרת:** {section.get('improved', '')}")

    st.write("### 💡 תוכנית פעולה")
    st.info(res.get('action_plan', ""))

    # שלב 4: הורדת Word
    st.divider()
    st.subheader("📥 שלב 4: הורדת קורות חיים משופרים")
    if st.button("צור קובץ Word להורדה"):
        try:
            docx_data = create_improved_docx(st.session_state.cv_text, res.get('improved_sections', []))
            st.download_button(
                label="לחצי כאן להורדת הקובץ 📄",
                data=docx_data,
                file_name="Improved_CV.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"שגיאה ביצירת הקובץ: {e}")