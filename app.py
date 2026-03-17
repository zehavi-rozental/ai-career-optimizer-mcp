import streamlit as st
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from docx import Document
from io import BytesIO
import re

st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# אתחול Session State
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "search_results" not in st.session_state: st.session_state.search_results = []
if "selected_job_description" not in st.session_state: st.session_state.selected_job_description = ""
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None

st.title("🎯 AI Career Optimizer Pro")

# שלב 1: קורות חיים (Sidebar)
with st.sidebar:
    st.header("📄 שלב 1: קורות חיים")
    if not st.session_state.cv_text:
        pdf_file = st.file_uploader("העלי קורות חיים (PDF)", type=['pdf'])
        if pdf_file:
            st.session_state.cv_text = extract_text_from_pdf(pdf_file)
            st.rerun()
    else:
        st.success("✅ קורות חיים טעונים")
        if st.button("החלף קובץ"):
            st.session_state.cv_text = ""
            st.rerun()

# שלב 2: חיפוש משרות עם תיאור מלא וקישור
st.subheader("🔍 שלב 2: פיד משרות מותאם")
query = st.text_input("איזה תפקיד את מחפשת?", placeholder="למשל: Fullstack Developer")

if st.button("מצא לי משרות רלוונטיות", type="primary"):
    with st.spinner("סורק משרות מפורטות..."):
        st.session_state.search_results = GoogleSearchService.search_jobs(query)

if st.session_state.search_results:
    st.write(f"### נמצאו {len(st.session_state.search_results)} משרות רלוונטיות:")
    for i, job in enumerate(st.session_state.search_results):
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"#### {job.get('title')}")
                # "וילון" שנפתח עם התיאור המלא
                with st.expander("📖 קראי את תיאור המשרה המלא"):
                    full_desc = job.get('snippet', 'אין תיאור זמין')
                    st.write(full_desc)
                    st.link_button("🔗 למקור המשרה", job.get('link', '#'))
            with col2:
                if st.button("בחר לניתוח 🎯", key=f"btn_{i}"):
                    st.session_state.selected_job_description = job.get('snippet', '')
                    st.toast("המשרה נבחרה!")

st.markdown("---")

# שלב 3: ניתוח AI עם מד התאמה והורדה ל-Word
st.subheader("📊 שלב 3: ניתוח התאמה ושיפור")
job_input = st.text_area("תיאור המשרה שנבחרה:", value=st.session_state.selected_job_description, height=150)

if st.button("🚀 נתח ושפר בירוק", type="primary"):
    if job_input and st.session_state.cv_text:
        with st.spinner("ה-AI מנתח..."):
            st.session_state.analysis_results = AIService.analyze_job_match(st.session_state.cv_text, job_input)

if st.session_state.analysis_results:
    # חילוץ ציון והצגת Progress Bar
    score_match = re.search(r"SCORE:\s*(\d+)", st.session_state.analysis_results)
    if score_match:
        score = int(score_match.group(1))
        st.metric("ציון התאמה", f"{score}%")
        st.progress(score / 100)

    st.markdown("---")
    st.write(st.session_state.analysis_results, unsafe_allow_html=True)

    # הורדה ל-Word
    doc = Document()
    doc.add_heading('דוח ניתוח משרה', 0)
    doc.add_paragraph(re.sub('<[^<]+?>', '', st.session_state.analysis_results))
    bio = BytesIO()
    doc.save(bio)
    st.download_button("📥 הורדי ניתוח כ-Word", data=bio.getvalue(), file_name="analysis.docx")