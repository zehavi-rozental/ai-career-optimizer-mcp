import streamlit as st
import requests
import json
import PyPDF2
import io
from docx import Document
from docx.shared import RGBColor

# ==========================================
# 1. הגדרות דף ועיצוב (UI)
# ==========================================
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

api_key = st.secrets.get("GOOGLE_API_KEY")
search_id = st.secrets.get("SEARCH_ENGINE_ID")

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #ff4b4b; color: white; border: none; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #ff3333; transform: translateY(-2px); }
    .job-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #eee; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    .metric-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; border: 1px solid #eee; }
    .keyword-tag { display: inline-block; padding: 5px 12px; margin: 4px; border-radius: 20px; background-color: #ffeaea; color: #ff4b4b; font-weight: 600; border: 1px solid #ffcccc; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. פונקציות ליבה (Search, AI & Word)
# ==========================================

def google_search_jobs(query):
    if not query: return []
    url = "https://www.googleapis.com/customsearch/v1"
    params = {'q': query, 'key': api_key, 'cx': search_id, 'num': 5}
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            return response.json().get('items', [])
        return []
    except:
        return []


def get_ai_response(prompt, is_json=True):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"} if is_json else {}
    }
    try:
        res = requests.post(url, json=payload, params={'key': api_key}, timeout=30)
        return json.loads(res.json()['candidates'][0]['content']['parts'][0]['text'])
    except:
        return None


def create_improved_docx(diff_data):
    doc = Document()
    doc.add_heading('Improved CV - AI Career Optimizer', 0)

    doc.add_heading('Changes Explanation:', level=1)
    doc.add_paragraph(diff_data.get('explanation', 'Adjustments made for ATS optimization.'))

    doc.add_heading('Marked Version:', level=1)
    p = doc.add_paragraph()

    for part, status in diff_data.get('diff', []):
        run = p.add_run(part)
        if status == 'add':
            run.font.color.rgb = RGBColor(0, 128, 0)  # Green
            run.bold = True
        elif status == 'remove':
            run.font.color.rgb = RGBColor(255, 0, 0)  # Red
            run.font.strike = True

    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio


# ==========================================
# 3. ניהול מצב (Session State)
# ==========================================
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "job_desc" not in st.session_state: st.session_state.job_desc = ""
if "search_results" not in st.session_state: st.session_state.search_results = []

# ==========================================
# 4. ממשק משתמש
# ==========================================

with st.sidebar:
    st.title("⚙️ הגדרות")
    pdf_file = st.file_uploader("📄 שלב 1: העלאת קורות חיים", type=['pdf'])
    if pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        st.session_state.cv_text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        st.success("קורות החיים נטענו!")

st.title("🎯 AI Career Optimizer Pro")

if not st.session_state.cv_text:
    st.info("👈 התחילי בהעלאת קורות חיים בסרגל הצדי.")
    st.stop()

# --- שלב החיפוש ---
st.subheader("🔍 שלב 2: מציאת משרה")
col1, col2 = st.columns([3, 1])
query = col1.text_input("איזו משרה נחפש?", placeholder="למשל: מנהלת משרד...")

if col2.button("🔎 חפשי משרות"):
    with st.spinner("סורק אתרי דרושים..."):
        st.session_state.search_results = google_search_jobs(query)

if st.session_state.search_results:
    for i, item in enumerate(st.session_state.search_results):
        with st.container():
            st.markdown(
                f'<div class="job-card"><h4><a href="{item["link"]}" target="_blank">{item["title"]}</a></h4><p>{item["snippet"]}</p></div>',
                unsafe_allow_html=True)
            if st.button(f"בחרי משרה #{i + 1}", key=f"select_{i}"):
                st.session_state.job_desc = item['snippet']
                st.success("המשרה נבחרה!")

st.divider()

# --- שלב הניתוח ---
st.subheader("📊 שלב 3: ניתוח והתאמה")
job_input = st.text_area("תיאור המשרה:", value=st.session_state.job_desc, height=150)

if st.button("⚡ הרץ ניתוח עמוק"):
    if job_input:
        with st.spinner("מנתח..."):
            prompt = f"CV: {st.session_state.cv_text[:2000]} Job: {job_input}. Return JSON: {{'score': 0-100, 'missing_skills': [], 'action_plan': 'Hebrew advice'}}"
            res = get_ai_response(prompt)
            if res:
                c1, c2 = st.columns([1, 2])
                c1.metric("ציון התאמה", f"{res['score']}%")
                c2.write(f"**תוכנית פעולה:** {res['action_plan']}")
                st.write("**מילות מפתח חסרות:**")
                st.markdown(" ".join([f'<span class="keyword-tag">{kw}</span>' for kw in res['missing_skills']]),
                            unsafe_allow_html=True)

st.divider()

# --- שלב ה-Word ---
st.subheader("📝 שלב 4: הורדת קורות חיים משופרים")
if st.button("🪄 ייצר קובץ Word לעריכה"):
    with st.spinner("ה-AI משכתב ומסמן שינויים..."):
        prompt = f"""
        Compare CV: {st.session_state.cv_text[:2000]} to Job: {job_input}.
        Rewrite the CV. Return JSON with 'diff' (list of [text, status]) and 'explanation'.
        Status: 'keep', 'add' (green), 'remove' (red/strike).
        """
        res = get_ai_response(prompt)
        if res:
            doc_file = create_improved_docx(res)
            st.download_button("📥 הורדי קובץ Word", data=doc_file, file_name="Improved_CV.docx",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")