import streamlit as st
import os
import json
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from utils.docx_generator import create_improved_docx

# הגדרות דף
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# טעינת עיצוב
css_path = os.path.join("assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# אתחול Session State
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "search_results" not in st.session_state: st.session_state.search_results = []
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None

# סרגל צדי
with st.sidebar:
    st.title("⚙️ Settings")
    pdf_file = st.file_uploader("📄 Step 1: Upload CV (PDF)", type=['pdf'])
    if pdf_file:
        with st.spinner("Extracting text..."):
            st.session_state.cv_text = extract_text_from_pdf(pdf_file)
            st.success("✅ CV Loaded!")

st.title("🎯 AI Career Optimizer Pro")

# שלב 2: חיפוש משרות
st.subheader("🔍 Step 2: Find a Job")
col1, col2 = st.columns([3, 1])
query = col1.text_input("What role are we looking for?", placeholder="e.g. Developer")

if col2.button("🔎 Search Jobs", type="primary"):
    if query:
        with st.spinner("Searching..."):
            st.session_state.search_results = GoogleSearchService.search_jobs(query)
    else:
        st.error("Please enter a job title")

if st.session_state.search_results:
    for item in st.session_state.search_results:
        st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <h4>{item['title']}</h4>
                <a href="{item['link']}" target="_blank">Open Search 🚀</a>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# שלב 3: ניתוח
st.subheader("📊 Step 3: Match Analysis")
job_input = st.text_area("Paste Job Description here:", height=150)

if st.button("🚀 Run Analysis", type="primary"):
    if not job_input or not st.session_state.cv_text:
        st.error("Missing CV or Job Description!")
    else:
        with st.spinner("Analyzing..."):
            prompt = f"Analyze CV vs Job Description. Return JSON: score, missing_skills, action_plan. CV: {st.session_state.cv_text[:3000]} Job: {job_input}"
            res = AIService.get_response(prompt)
            if res:
                st.session_state.analysis_results = res

if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    st.metric("Match Score", f"{res.get('score', 0)}%")
    st.subheader("Missing Skills")
    for s in res.get('missing_skills', []):
        st.write(f"- {s}")
    st.subheader("Action Plan")
    st.write(res.get('action_plan', ""))