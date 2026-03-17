import streamlit as st
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from docx import Document
from io import BytesIO
import re


# פונקציה ליצירת קובץ Word
def create_word_doc(analysis_text):
    doc = Document()
    doc.add_heading('דוח ניתוח ושיפור קורות חיים - AI Optimizer', 0)
    # ניקוי תגיות ה-HTML לפני השמירה ל-Word
    clean_text = re.sub('<[^<]+?>', '', analysis_text)
    doc.add_paragraph(clean_text)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()


# הגדרות דף
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# אתחול Session State
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "search_results" not in st.session_state: st.session_state.search_results = []
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None
if "selected_job_description" not in st.session_state: st.session_state.selected_job_description = ""

st.title("🎯 AI Career Optimizer Pro")
st.markdown("---")

# שלב 1: העלאת קורות חיים
with st.sidebar:
    st.header("📄 שלב 1: קורות חיים")
    if st.session_state.cv_text:
        st.success("✅ קורות חיים שמורים")
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

# שלב 2: חיפוש משרות
st.subheader("🔍 שלב 2: פיד משרות")
query = st.text_input("איזה תפקיד את מחפשת?", placeholder="למשל: Full Stack Developer")

if st.button("מצא לי משרות", type="primary"):
    if query:
        with st.spinner("סורק משרות ברשת..."):
            results = GoogleSearchService.search_jobs(query)
            st.session_state.search_results = results

if st.session_state.search_results:
    for i, job in enumerate(st.session_state.search_results):
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader(job.get('title'))
                st.write(job.get('snippet'))
            with col2:
                if st.button("בחר לניתוח 🎯", key=f"sel_{i}"):
                    st.session_state.selected_job_description = job.get('snippet', '')
                    st.toast("המשרה נבחרה!")
                    st.rerun()

st.markdown("---")

# שלב 3: ניתוח התאמה
st.subheader("📊 שלב 3: ניתוח התאמה ושיפור (AI)")

with st.expander("📝 צפייה/עריכה של תיאור המשרה המלא", expanded=True):
    job_input = st.text_area("תיאור המשרה:", value=st.session_state.selected_job_description, height=250)

if st.button("🚀 נתח ושפר את קורות החיים שלי", type="primary"):
    if job_input and st.session_state.cv_text:
        with st.spinner("סוכן ה-AI מנתח התאמה..."):
            analysis = AIService.analyze_job_match(st.session_state.cv_text, job_input)
            if analysis:
                st.session_state.analysis_results = analysis

if st.session_state.analysis_results:
    # חילוץ הציון מתוך הטקסט
    score_match = re.search(r"SCORE:\s*(\d+)", st.session_state.analysis_results)
    if score_match:
        score = int(score_match.group(1))
        st.write(f"### ציון התאמה: {score}%")
        st.progress(score / 100)
        # ניקוי שורת ה-SCORE מהתצוגה
        display_text = st.session_state.analysis_results.split("\n", 1)[-1]
    else:
        display_text = st.session_state.analysis_results

    st.markdown("---")
    # הצגת הטקסט עם תמיכה ב-HTML (בשביל הירוק)
    st.write(display_text, unsafe_allow_html=True)

    # אפשרות הורדה ל-Word
    st.markdown("---")
    word_data = create_word_doc(st.session_state.analysis_results)
    st.download_button(
        label="📥 הורדי את דוח השיפור כקובץ Word",
        data=word_data,
        file_name="Resume_Optimization_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )