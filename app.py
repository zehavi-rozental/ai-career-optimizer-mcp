import streamlit as st
import os
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from utils.docx_generator import create_improved_docx

# ==========================================
# 1. הגדרות דף (Page Config)
# ==========================================
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# ==========================================
# 2. טעינת עיצוב (Load CSS)
# ==========================================
css_path = os.path.join("assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==========================================
# 3. אתחול משתני מערכת (Session State)
# ==========================================
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "job_desc" not in st.session_state: st.session_state.job_desc = ""
if "search_results" not in st.session_state: st.session_state.search_results = []

# ==========================================
# 4. סרגל צדי - שלב 1 (Sidebar)
# ==========================================
with st.sidebar:
    st.title("⚙️ Settings")
    pdf_file = st.file_uploader("📄 Step 1: Upload CV", type=['pdf'])
    if pdf_file:
        st.session_state.cv_text = extract_text_from_pdf(pdf_file)
        st.success("CV Loaded Successfully!")

# ==========================================
# 5. ממשק ראשי
# ==========================================
st.title("🎯 AI Career Optimizer Pro")

if not st.session_state.cv_text:
    st.info("👈 Please start by uploading your CV in the sidebar.")
    st.stop()

# --- שלב 2: חיפוש משרות ---
st.subheader("🔍 Step 2: Find a Job")
col1, col2 = st.columns([3, 1])
query = col1.text_input("What role are we looking for?", placeholder="e.g. מנהלת משרד")

if col2.button("🔎 Search Jobs"):
    with st.spinner("Searching for opportunities..."):
        # קריאה למחלקה מתוך services/google_search.py
        results = GoogleSearchService.search_jobs(query)
        st.session_state.search_results = results

# הצגת תוצאות החיפוש
if st.session_state.search_results:
    for i, item in enumerate(st.session_state.search_results):
        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <h4><a href="{item['link']}" target="_blank">{item['title']}</a></h4>
                <p>{item['snippet']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Analyze Job #{i+1}", key=f"select_{i}"):
                st.session_state.job_desc = item['snippet']
                st.success("Job details captured! Scroll down for analysis.")

st.divider()

# --- שלב 3: ניתוח התאמה ---
st.subheader("📊 Step 3: Match Analysis")
job_input = st.text_area("Job Description:", value=st.session_state.job_desc, height=150)

if st.button("⚡ Run Deep ATS Analysis"):
    if job_input:
        with st.spinner("AI is analyzing the fit..."):
            analysis_prompt = f"""
            Analyze this CV against the Job Description. 
            CV: {st.session_state.cv_text[:3000]}
            JD: {job_input}
            Return JSON with: 'score' (0-100), 'missing_skills' (list), 'action_plan' (Hebrew text).
            """
            res = AIService.get_response(analysis_prompt)
            if res:
                c1, c2 = st.columns([1, 2])
                c1.metric("Match Score", f"{res['score']}%")
                c2.write(f"**Action Plan:** {res['action_plan']}")
                st.write("**Missing Keywords:**")
                st.markdown(" ".join([f'<span class="keyword-tag">{kw}</span>' for kw in res['missing_skills']]), unsafe_allow_html=True)
            else:
                st.error("Analysis failed. Please try again.")

st.divider()

# --- שלב 4: הורדת קובץ Word משופר ---
st.subheader("📝 Step 4: Download Tailored CV")
if st.button("🪄 Generate Word Document"):
    if not job_input:
        st.warning("Please provide a job description first.")
    else:
        with st.spinner("Optimizing your CV for this role..."):
            tailor_prompt = f"""
            Compare CV: {st.session_state.cv_text[:2000]} to Job: {job_input}. 
            Rewrite the CV professionally. Return JSON with 'diff' (list of [text, status]) and 'explanation'.
            Status options: 'keep', 'add' (for improvements), 'remove' (for unnecessary parts).
            """
            res = AIService.get_response(tailor_prompt)
            if res:
                doc_file = create_improved_docx(res)
                st.download_button(
                    label="📥 Download Word File",
                    data=doc_file,
                    file_name="Tailored_CV.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )