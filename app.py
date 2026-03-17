import streamlit as st
import os
import json
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from utils.docx_generator import create_improved_docx

# הגדרות דף - חובה כפקודה ראשונה
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
        with st.spinner("מחלץ טקסט..."):
            text = extract_text_from_pdf(pdf_file)
            if text:
                st.session_state.cv_text = text
                st.success("✅ קורות החיים נטענו!")

# שלב 2: לוח משרות
st.subheader("🔍 שלב 2: לוח משרות חכם")
query = st.text_input("איזה תפקיד את מחפשת?", placeholder="Junior Full Stack Developer")

if st.button("חפש משרות", type="primary"):
    if query:
        with st.spinner("מחפש..."):
            st.session_state.search_results = GoogleSearchService.search_jobs(query)

if st.session_state.search_results:
    st.write("### בחרי לוח משרות:")
    cols = st.columns(4)  # פריסה ל-4 עמודות כפי שביקשת
    for i, item in enumerate(st.session_state.search_results):
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"#### {item['source']}")
                st.link_button(f"פתח ב-{item['source']} 🚀", item['link'])

st.divider()

# שלב 3: ניתוח
st.subheader("📊 שלב 3: ניתוח והתאמה")
job_input = st.text_area("הדביקי תיאור משרה:", height=150)

if st.button("🚀 נתח ושפר את קורות החיים שלי", type="primary"):
    if not job_input or not st.session_state.cv_text:
        st.error("חסר מידע.")
    else:
        with st.spinner("מנתח..."):
            # שימוש בטקסט אנגלי בלבד בהוראות למניעת שגיאות 400
            prompt = f"""
            Task: Compare CV and Job Description.
            Return ONLY a JSON object.
            Format: {{"score": 80, "missing_skills": [], "action_plan": "", "improved_sections": []}}
            CV: {st.session_state.cv_text[:2000]}
            Job: {job_input[:2000]}
            """
            res = AIService.get_response(prompt)
            if res:
                st.session_state.analysis_results = res

if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    st.metric("ציון התאמה", f"{res.get('score', 0)}%")

    st.write("### 📝 דו\"ח שיפור")
    for section in res.get('improved_sections', []):
        # כתיבה בשורה אחת למניעת SyntaxError
        with st.expander(f"שיפור: {section.get('explanation', '')[:50]}"):
            st.markdown(f"**❌ מקור:** {section.get('original', '')}")
            st.success(f"**✅ משופר:** {section.get('improved', '')}")

    if st.button("הורד קובץ Word"):
        data = create_improved_docx(st.session_state.cv_text, res.get('improved_sections', []))
        st.download_button("לחצי להורדה", data, "CV_Fixed.docx")