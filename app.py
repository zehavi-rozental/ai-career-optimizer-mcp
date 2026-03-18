import streamlit as st
from services.google_search import GoogleSearchService
from services.ai_service import AIService
from utils.pdf_processor import extract_text_from_pdf, extract_text_from_docx
from docx import Document
from io import BytesIO
import re

st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# אתחול Session State
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'selected_job_description' not in st.session_state:
    st.session_state.selected_job_description = ""
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

st.title("🎯 AI Career Optimizer Pro")

# שלב 1: העלאת קורות חיים
st.markdown("## 📄 שלב 1: העלאת קורות חיים")
uploaded_file = st.file_uploader("העלי את קורות החיים שלך (PDF או DOCX):", type=["pdf", "docx"])

if uploaded_file is not None:
    with st.spinner("מעבד את הקובץ..."):
        if uploaded_file.name.endswith('.pdf'):
            st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            st.session_state.resume_text = extract_text_from_docx(uploaded_file)
    st.success("✅ קורות חיים נטענו בהצלחה!")

st.divider()

# שלב 2: חיפוש משרות ספציפיות
st.markdown("## 🔍 שלב 2: חיפוש משרות ספציפיות")
col_search, col_btn = st.columns([4, 1])
with col_search:
    job_query = st.text_input("איזו משרה את מחפשת?", value=st.session_state.search_query)
with col_btn:
    st.write(" ")
    if st.button("🔎 חפש משרות", use_container_width=True):
        st.session_state.current_page = 1
        st.session_state.search_query = job_query
        with st.spinner("מחפש משרות רלוונטיות..."):
            results = GoogleSearchService.search_jobs(job_query, page=1)
            st.session_state.search_results = results

# הצגת תוצאות החיפוש עם דפדוף וטעינת תיאור מלא
if st.session_state.search_results:
    st.subheader(f"📋 תוצאות חיפוש (עמוד {st.session_state.current_page})")

    for i, job in enumerate(st.session_state.search_results):
        with st.expander(f"📖 {job.get('title', 'ללא כותרת')} - {job.get('display_link', '')}"):
            st.markdown(f"**תיאור קצר:** {job.get('snippet', 'אין תיאור זמין')}")

            col_fetch, col_select = st.columns([1, 1])
            with col_fetch:
                if st.button(f"⬇️ שאוב תיאור מלא", key=f"fetch_{i}"):
                    with st.spinner("שואב תיאור משרה מלא מהאתר..."):
                        full_text = GoogleSearchService.get_full_job_content(job.get('link'))
                        st.session_state.selected_job_description = full_text
                        st.toast("✅ התיאור המלא נטען לשלב 3!")

            with col_select:
                if st.button(f"✅ בחר לניתוח", key=f"select_{i}"):
                    st.session_state.selected_job_description = job.get('snippet', '')
                    st.toast("💾 המשרה נבחרה!")

            st.link_button("🔗 למשרה המלאה באתר", job.get('link', '#'))

    # כפתורי דפדוף
    col_prev, col_page, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.session_state.current_page > 1:
            if st.button("⬅️ עמוד קודם"):
                st.session_state.current_page -= 1
                st.session_state.search_results = GoogleSearchService.search_jobs(
                    st.session_state.search_query, page=st.session_state.current_page
                )
                st.rerun()
    with col_page:
        st.write(f"<div align='center'>עמוד {st.session_state.current_page}</div>", unsafe_allow_html=True)
    with col_next:
        if st.button("עמוד הבא ➡️"):
            st.session_state.current_page += 1
            st.session_state.search_results = GoogleSearchService.search_jobs(
                st.session_state.search_query, page=st.session_state.current_page
            )
            st.rerun()

st.divider()

# שלב 3: ניתוח התאמה ושיפור
st.markdown("## 📊 שלב 3: ניתוח התאמה ושיפור")
st.write("*בדוק את תיאור המשרה לפני ניתוח:*")
job_desc_input = st.text_area(
    "תיאור המשרה (התיאור המלא ייטען כאן אחרי לחיצה על 'שאוב'):",
    value=st.session_state.selected_job_description,
    height=400,
    max_chars=5000
)

if st.button("🚀 נתחי התאמה ושפרי קורות חיים", type="primary"):
    if not st.session_state.resume_text or not job_desc_input:
        st.error("❌ אנא וודאי שהעלית קורות חיים ובחרת משרה.")
    else:
        with st.spinner("🤖 ה-AI מנתח בעומק..."):
            st.session_state.analysis_results = AIService.analyze_job_match(st.session_state.resume_text, job_desc_input)

if st.session_state.analysis_results:
    # חילוץ ציון והצגת Progress Bar
    score_match = re.search(r"SCORE:\s*(\d+)", st.session_state.analysis_results)
    if score_match:
        score = int(score_match.group(1))
        st.metric("📈 ציון התאמה", f"{score}%")
        st.progress(score / 100)

    st.markdown("---")
    st.markdown(st.session_state.analysis_results, unsafe_allow_html=True)

    # הורדה ל-Word
    doc = Document()
    doc.add_heading('דוח ניתוח משרה - AI Career Optimizer', 0)
    doc.add_paragraph(re.sub('<[^<]+?>', '', st.session_state.analysis_results))
    bio = BytesIO()
    doc.save(bio)
    bio.seek(0)
    st.download_button(
        label="📥 הורדי ניתוח כ-Word",
        data=bio.getvalue(),
        file_name="job_analysis.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
