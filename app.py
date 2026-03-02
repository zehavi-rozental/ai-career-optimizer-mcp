import streamlit as st
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from utils.docx_generator import create_improved_docx

# 1. Page Config
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# 2. Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Session State Init
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "job_desc" not in st.session_state: st.session_state.job_desc = ""
if "search_results" not in st.session_state: st.session_state.search_results = []

# 4. Sidebar - Step 1
with st.sidebar:
    st.title("⚙️ Settings")
    pdf_file = st.file_uploader("📄 Step 1: Upload CV", type=['pdf'])
    if pdf_file:
        st.session_state.cv_text = extract_text_from_pdf(pdf_file)
        st.success("CV Loaded Successfully!")

st.title("🎯 AI Career Optimizer Pro")

if not st.session_state.cv_text:
    st.info("👈 Please start by uploading your CV in the sidebar.")
    st.stop()

# 5. Search - Step 2
st.subheader("🔍 Step 2: Find a Job")
col1, col2 = st.columns([3, 1])
query = col1.text_input("What role are we looking for?", placeholder="e.g. Office Manager...")

if col2.button("🔎 Search Jobs"):
    with st.spinner("Searching..."):
        st.session_state.search_results = GoogleSearchService.search_jobs(query)

if st.session_state.search_results:
    for i, item in enumerate(st.session_state.search_results):
        with st.container():
            st.markdown(f'<div class="job-card"><h4><a href="{item["link"]}" target="_blank">{item["title"]}</a></h4><p>{item["snippet"]}</p></div>', unsafe_allow_html=True)
            if st.button(f"Analyze Job #{i+1}", key=f"select_{i}"):
                st.session_state.job_desc = item['snippet']
                st.success("Job details captured!")

st.divider()

# 6. Analysis - Step 3
st.subheader("📊 Step 3: Match Analysis")
job_input = st.text_area("Job Description:", value=st.session_state.job_desc, height=150)

if st.button("⚡ Run Deep ATS Analysis"):
    if job_input:
        with st.spinner("AI Analyzing..."):
            prompt = f"CV: {st.session_state.cv_text[:2000]} Job: {job_input}. Return JSON: {{'score': 0-100, 'missing_skills': [], 'action_plan': 'Hebrew advice'}}"
            res = AIService.get_response(prompt)
            if res:
                c1, c2 = st.columns([1, 2])
                c1.metric("Match Score", f"{res['score']}%")
                c2.write(f"**Action Plan:** {res['action_plan']}")
                st.write("**Missing Keywords:**")
                st.markdown(" ".join([f'<span class="keyword-tag">{kw}</span>' for kw in res['missing_skills']]), unsafe_allow_html=True)

st.divider()

# 7. Export - Step 4
st.subheader("📝 Step 4: Download Tailored CV")
if st.button("🪄 Generate Word Document"):
    with st.spinner("Tailoring CV..."):
        prompt = f"Compare CV: {st.session_state.cv_text[:2000]} to Job: {job_input}. Rewrite. Return JSON with 'diff' (list of [text, status]) and 'explanation'. Status: 'keep', 'add', 'remove'."
        res = AIService.get_response(prompt)
        if res:
            doc_file = create_improved_docx(res)
            st.download_button("📥 Download Word File", data=doc_file, file_name="Tailored_CV.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")