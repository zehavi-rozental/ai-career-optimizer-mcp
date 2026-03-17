import streamlit as st
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from docx import Document
from io import BytesIO
import re

st.set_page_config(page_title="Career Optimizer Pro", page_icon="🎯", layout="wide")

if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "search_results" not in st.session_state: st.session_state.search_results = []
if "selected_job_description" not in st.session_state: st.session_state.selected_job_description = ""
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None

st.title("🎯 AI Career Optimizer Pro")

# שלב 1: קורות חיים
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

# שלב 2: חיפוש עם וילונות (Expanders)
st.subheader("🔍 שלב 2: פיד משרות מותאם")
query = st.text_input("איזה תפקיד את מחפשת?", placeholder="למשל: Junior Developer")

if st.button("מצא לי משרות רלוונטיות", type="primary"):
    with st.spinner("סורק משרות מפורטות..."):
        st.session_state.search_results = GoogleSearchService.search_jobs(query)

if st.session_state.search_results:
    st.write(f"### נמצאו {len(st.session_state.search_results)} משרות:")
    for i, job in enumerate(st.session_state.search_results[:10]):
        with st.container(border=True):
            # כותרת המשרה בחוץ
            st.markdown(f"### {job.get('title')}")

            # ה"וילון" שנפתח עם התיאור המלא
            with st.expander("📖 קראי את תיאור המשרה המלא"):
                full_desc = job.get('snippet', 'אין תיאור זמין')
                st.write(full_desc)
                st.link_button("🔗 למקור המשרה", job.get('link', '#'))

            # כפתור בחירה לניתוח
            if st.button("בחר לניתוח 🎯", key=f"job_btn_{i}"):
                st.session_state.selected_job_description = job.get('snippet', '')
                st.toast("המשרה נבחרה!")

st.markdown("---")

# שלב 3: ניתוח והצגת תוצאות
st.subheader("📊 שלב 3: ניתוח התאמה")
job_input = st.text_area("תיאור המשרה שנבחרה (ניתן לערוך):",
                         value=st.session_state.selected_job_description,
                         height=250)

if st.button("🚀 נתחי ושפרי בירוק", type="primary"):
    if job_input and st.session_state.cv_text:
        with st.spinner("ה-AI מנתח לעומק..."):
            st.session_state.analysis_results = AIService.analyze_job_match(st.session_state.cv_text, job_input)

if st.session_state.analysis_results:
    # הצגת ציון ויזואלי (Gauge)
    score_match = re.search(r"SCORE:\s*(\d+)", st.session_state.analysis_results)
    if score_match:
        score = int(score_match.group(1))
        st.metric("ציון התאמה", f"{score}%")
        st.progress(score / 100)

    st.markdown("---")
    # הצגת הניתוח עם תמיכה ב-HTML לצבע הירוק
    st.markdown(st.session_state.analysis_results, unsafe_allow_html=True)

    # ייצוא ל-Word
    doc = Document()
    doc.add_heading('דוח ניתוח משרה', 0)
    clean_text = re.sub('<[^<]+?>', '', st.session_state.analysis_results)
    doc.add_paragraph(clean_text)
    bio = BytesIO()
    doc.save(bio)
    st.download_button("📥 הורדי כ-Word", data=bio.getvalue(), file_name="analysis.docx")