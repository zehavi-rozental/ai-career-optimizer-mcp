import streamlit as st
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf

# 1. הגדרות דף
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# 2. אתחול Session State
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "search_results" not in st.session_state: st.session_state.search_results = []
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None
if "selected_job_description" not in st.session_state: st.session_state.selected_job_description = ""

st.title("🎯 AI Career Optimizer Pro")
st.markdown("---")

# שלב 1: קורות חיים
with st.sidebar:
    st.header("📄 שלב 1: קורות חיים")
    if st.session_state.cv_text:
        st.success("✅ קורות חיים שמורים במערכת")
        if st.button("העלה קובץ חדש"):
            st.session_state.cv_text = ""
            st.rerun()
    else:
        pdf_file = st.file_uploader("העלי קובץ PDF", type=['pdf'])
        if pdf_file:
            with st.spinner("מחלץ טקסט..."):
                text = extract_text_from_pdf(pdf_file)
                if text:
                    st.session_state.cv_text = text
                    st.rerun()

# שלב 2: פיד משרות
st.subheader("🔍 שלב 2: פיד משרות ממוקד")
query = st.text_input("איזה תפקיד את מחפשת?", placeholder="למשל: Junior Full Stack Developer")

if st.button("מצא לי משרות רלוונטיות", type="primary"):
    if query:
        with st.spinner("סורק משרות..."):
            results = GoogleSearchService.search_jobs(query)
            st.session_state.search_results = results

if st.session_state.search_results:
    st.write(f"### נמצאו {len(st.session_state.search_results)} תוצאות:")
    for i, job in enumerate(st.session_state.search_results):
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader(job.get('title'))
                st.write(job.get('snippet'))
            with col2:
                if st.button("בחר לניתוח 🎯", key=f"select_{i}"):
                    st.session_state.selected_job_description = job.get('snippet', '')
                    st.toast("המשרה נבחרה!")
                    st.rerun()
                st.link_button("למשרה 🔗", job.get('link'))

st.markdown("---")

# שלב 3: ניתוח AI
st.subheader("📊 שלב 3: ניתוח התאמה (AI)")
job_input = st.text_area("תיאור המשרה:", value=st.session_state.selected_job_description, height=150)

if st.button("🚀 נתח התאמה", type="primary"):
    if job_input and st.session_state.cv_text:
        with st.spinner("מנתח..."):
            analysis = AIService.analyze_job_match(st.session_state.cv_text, job_input)
            st.session_state.analysis_results = analysis

if st.session_state.analysis_results:
    st.info("### 📋 דוח ניתוח משרה")
    st.markdown(st.session_state.analysis_results)