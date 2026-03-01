import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import json
import PyPDF2
from datetime import datetime

# ==========================================
# 1. PAGE CONFIG & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="AI Career Assistant", page_icon="🚀", layout="wide")

# משיכת המפתח מה-Secrets (מוגדר בלוח הבקרה של Streamlit)
api_key = st.secrets.get("GOOGLE_API_KEY")

custom_css = """
<style>
    .metric-card {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
    }
    .metric-value { font-size: 3rem; font-weight: bold; margin: 0; }
    .cv-add { color: #00FF00; font-weight: bold; background-color: rgba(0,255,0,0.1); padding: 2px 4px; border-radius: 3px; }
    .cv-del { color: #FF0000; text-decoration: line-through; background-color: rgba(255,0,0,0.1); padding: 2px 4px; border-radius: 3px; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE
# ==========================================
if "cv_text" not in st.session_state:
    st.session_state.cv_text = ""
if "job_history" not in st.session_state:
    st.session_state.job_history = []


# ==========================================
# 3. CORE LOGIC
# ==========================================

def extract_pdf_text(file) -> str:
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error: {e}"


def fetch_job_details(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all(['p', 'li', 'h1', 'h2'])
        content = "\n".join([p.get_text(strip=True) for p in paragraphs])
        return content if len(content) > 100 else "SCRAPE_BLOCKED"
    except:
        return "SCRAPE_FAILED"


def compare_skills(cv_text: str, job_desc: str, key: str) -> dict:
    genai.configure(api_key=key)
    # תיקון: הוספת סוגריים () אחרי GenerativeModel
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        generation_config={"response_mime_type": "application/json"}
    )

    prompt = f"""
    Analyze this CV against the Job Description. Return JSON:
    {{
        "match_score": <int 0-100>,
        "shared_skills": [],
        "missing_keywords": [],
        "role_relevance": "summary"
    }}
    CV: {cv_text}
    JD: {job_desc}
    """
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}


def generate_tailored_cv(cv_text: str, job_desc: str, key: str) -> str:
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    prompt = f"""
    Rewrite the CV to pass ATS for this job. 
    Use <span class='cv-add'>text</span> for additions and <span class='cv-del'>text</span> for deletions.
    CV: {cv_text}
    JD: {job_desc}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


# ==========================================
# 4. GUI
# ==========================================

with st.sidebar:
    st.header("⚙️ Settings")
    # אם המפתח לא נמצא ב-Secrets, נאפשר להזין ידנית
    if not api_key:
        api_key = st.text_input("Enter Gemini API Key", type="password")
    else:
        st.success("API Key loaded from Secrets ✅")

    st.divider()
    st.header("📄 CV Source")
    upload_method = st.radio("Method", ["Upload PDF", "Paste Text"])

    if upload_method == "Upload PDF":
        uploaded_file = st.file_uploader("Choose PDF", type=['pdf'])
        if uploaded_file and st.button("Extract PDF"):
            st.session_state.cv_text = extract_pdf_text(uploaded_file)
    else:
        cv_input = st.text_area("Paste CV")
        if st.button("Save CV"):
            st.session_state.cv_text = cv_input

# Main Dashboard
st.title("🚀 CareerAssistant.ai")

if not api_key:
    st.warning("⚠️ Please provide an API Key to start.")
    st.stop()
if not st.session_state.cv_text:
    st.info("👈 Please upload your CV in the sidebar.")
    st.stop()

st.subheader("1. Job Targeting")
job_url = st.text_input("Job URL")
job_desc_input = st.text_area("Job Description", height=150)

if st.button("⚡ Run Analysis", type="primary"):
    if not job_desc_input:
        st.error("Please provide a job description.")
    else:
        with st.spinner("AI is working..."):
            analysis = compare_skills(st.session_state.cv_text, job_desc_input, api_key)
            optimized = generate_tailored_cv(st.session_state.cv_text, job_desc_input, api_key)

            if "error" in analysis:
                st.error(f"Error: {analysis['error']}")
            else:
                st.session_state.job_history.append({
                    "date": datetime.now().strftime("%H:%M"),
                    "score": analysis.get("match_score", 0)
                })

                st.divider()
                st.subheader("2. Results")

                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(
                        f'<div class="metric-card"><p class="metric-value">{analysis["match_score"]}%</p></div>',
                        unsafe_allow_html=True)
                with col2:
                    st.info(analysis["role_relevance"])

                st.subheader("3. Comparison")
                c1, c2 = st.columns(2)
                c1.success("✅ Skills Found: " + ", ".join(analysis["shared_skills"]))
                c2.error("❌ Missing: " + ", ".join(analysis["missing_keywords"]))

                st.subheader("4. Optimized CV")
                st.markdown(optimized, unsafe_allow_html=True)

st.divider()
st.subheader("5. History")
st.dataframe(st.session_state.job_history, use_container_width=True)