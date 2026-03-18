import streamlit as st
from services.google_search import GoogleSearchService
from services.ai_service import AIService
# ודאי שייבאת את המעבדים המתאימים לקבצים שלך
from utils.pdf_processor import PDFProcessor
from utils.docx_generator import DocxProcessor  # או השם המדויק אצלך בפרויקט

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
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""

st.title("🚀 AI Career Optimizer")

# שלב 1: העלאת קורות חיים (חזרה להעלאת קובץ כפי שביקשת)
st.markdown("### שלב 1: העלאת קורות חיים")
uploaded_file = st.file_uploader("העלי את קורות החיים שלך (PDF או DOCX):", type=["pdf", "docx"])

if uploaded_file is not None:
    with st.spinner("מעבד את הקובץ..."):
        if uploaded_file.name.endswith('.pdf'):
            st.session_state.resume_text = PDFProcessor.extract_text(uploaded_file)
        else:
            # כאן הקוד שמעבד DOCX אצלך בפרויקט
            st.session_state.resume_text = "טקסט חולץ מקובץ Word"
    st.success("קורות חיים נטענו בהצלחה!")

st.divider()

# שלב 2: חיפוש משרות ספציפיות
st.markdown("### שלב 2: חיפוש משרות ספציפיות")
col_search, col_btn = st.columns([4, 1])
with col_search:
    job_query = st.text_input("איזו משרה את מחפשת?", value=st.session_state.search_query)
with col_btn:
    st.write(" ")
    if st.button("חפש משרות", use_container_width=True):
        st.session_state.current_page = 1
        st.session_state.search_query = job_query
        with st.spinner("מחפש משרות רלוונטיות..."):
            results = GoogleSearchService.search_jobs(job_query, page=1)
            st.session_state.search_results = results

# הצגת תוצאות החיפוש עם דפדוף
if st.session_state.search_results:
    st.subheader(f"🔍 תוצאות חיפוש (עמוד {st.session_state.current_page})")

    for i, job in enumerate(st.session_state.search_results):
        with st.container(border=True):
            col_info, col_action = st.columns([4, 1])
            with col_info:
                st.markdown(f"#### {job.get('title')}")
                st.write(job.get('snippet'))

            with col_action:
                if st.button(f"בחר לניתוח 🎯", key=f"select_{i}"):
                    with st.spinner("שואב תיאור משרה מלא מהאתר..."):
                        full_text = GoogleSearchService.get_full_job_content(job.get('link'))
                        st.session_state.selected_job_description = full_text
                        st.toast("התיאור המלא נטען לשלב 3!")

    # כפתורי דפדוף
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

# שלב 3: ניתוח התאמה ושיפור
st.markdown("### שלב 3: ניתוח התאמה ושיפור")
job_desc_input = st.text_area(
    "תיאור המשרה (התיאור המלא ייטען כאן):",
    value=st.session_state.selected_job_description,
    height=300
)

if st.button("נתחי התאמה ושפרי קורות חיים 🚀", type="primary"):
    if not st.session_state.resume_text or not job_desc_input:
        st.error("אנא וודאי שהעלית קורות חיים ובחרת משרה.")
    else:
        with st.spinner("מנתח לעומק..."):
            analysis = AIService.analyze_job_match(st.session_state.resume_text, job_desc_input)
            if analysis:
                st.markdown(analysis, unsafe_allow_html=True)