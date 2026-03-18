import streamlit as st
from services.google_search import GoogleSearchService
from services.ai_service import AIService
import os

# הגדרת תצורת דף
st.set_page_config(page_title="AI Career Optimizer", page_icon="🚀", layout="wide")

# אתחול Session State לניהול נתונים בין הרצות
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'selected_job_description' not in st.session_state:
    st.session_state.selected_job_description = ""
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

st.title("🚀 AI Career Optimizer")
st.markdown("### שלב 1: העלאת קורות חיים")
resume_text = st.text_area("הדביקי כאן את קורות החיים שלך:", height=200)

st.divider()

st.markdown("### שלב 2: חיפוש משרות ספציפיות")
col_search, col_btn = st.columns([4, 1])
with col_search:
    job_query = st.text_input("איזו משרה את מחפשת? (למשל: Fullstack Developer Junior)",
                              value=st.session_state.search_query)
with col_btn:
    st.write(" ")  # מרווח לעיצוב
    if st.button("חפש משרות", use_container_width=True):
        st.session_state.current_page = 1
        st.session_state.search_query = job_query
        with st.spinner("מחפש משרות רלוונטיות..."):
            results = GoogleSearchService.search_jobs(job_query, page=1)
            st.session_state.search_results = results

# הצגת תוצאות החיפוש
if st.session_state.search_results:
    st.subheader(f"🔍 תוצאות חיפוש (עמוד {st.session_state.current_page})")

    for i, job in enumerate(st.session_state.search_results):
        with st.container(border=True):
            col_info, col_action = st.columns([4, 1])
            with col_info:
                st.markdown(f"#### {job.get('title')}")
                st.caption(f"מקור: {job.get('link')}")
                # הצגת התקציר הראשוני מגוגל
                st.write(job.get('snippet'))

            with col_action:
                if st.button(f"בחר לניתוח 🎯", key=f"select_{i}"):
                    with st.spinner("שואב תיאור משרה מלא מהאתר..."):
                        # שאיבת התוכן המלא מהקישור
                        full_text = GoogleSearchService.get_full_job_content(job.get('link'))
                        st.session_state.selected_job_description = full_text
                        st.toast("התיאور המלא נטען בהצלחה!")

    # מנגנון דפדוף (Pagination)
    col_prev, col_page, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.session_state.current_page > 1:
            if st.button("⬅️ 10 הקודמות"):
                st.session_state.current_page -= 1
                st.session_state.search_results = GoogleSearchService.search_jobs(
                    st.session_state.search_query, page=st.session_state.current_page
                )
                st.rerun()
    with col_page:
        st.write(f"<center>עמוד {st.session_state.current_page}</center>", unsafe_allow_html=True)
    with col_next:
        if st.button("10 הבאות ➡️"):
            st.session_state.current_page += 1
            st.session_state.search_results = GoogleSearchService.search_jobs(
                st.session_state.search_query, page=st.session_state.current_page
            )
            st.rerun()

st.divider()

st.markdown("### שלב 3: ניתוח התאמה ושיפור")
# תיבת הטקסט מתעדכנת אוטומטית כשבוחרים משרה
job_desc_input = st.text_area(
    "תיאור המשרה (כאן יופיע התיאור המלא שיישאב):",
    value=st.session_state.selected_job_description,
    height=300
)

if st.button("נתחי התאמה ושפרי קורות חיים 🚀", type="primary"):
    if not resume_text or not job_desc_input:
        st.error("אנא וודאי שהזנת קורות חיים ובחרת משרה (או הדבקת תיאור).")
    else:
        with st.spinner("מנתח לעומק... זה עשוי לקחת כמה שניות"):
            analysis = AIService.analyze_job_match(resume_text, job_desc_input)
            if analysis:
                st.markdown("---")
                st.markdown(analysis, unsafe_allow_html=True)