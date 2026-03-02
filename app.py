import streamlit as st
import requests
import json
import PyPDF2
from datetime import datetime

# ==========================================
# 1. הגדרות דף ועיצוב (UI)
# ==========================================
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# משיכת המפתחות מה-Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
search_id = st.secrets.get("SEARCH_ENGINE_ID")

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #ff4b4b; color: white; border: none; font-weight: bold; }
    .job-card {
        background: white; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #eee; 
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .metric-card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; border: 1px solid #eee;
    }
    .metric-value { font-size: 3.5rem; font-weight: 800; color: #ff4b4b; margin: 0; }
    .keyword-tag {
        display: inline-block; padding: 5px 12px; margin: 4px; border-radius: 20px;
        background-color: #ffeaea; color: #ff4b4b; font-weight: 600; border: 1px solid #ffcccc;
    }
    .cv-add { color: #28a745; font-weight: bold; background-color: #e6ffed; padding: 2px 4px; border-radius: 4px; }
    .cv-del { color: #dc3545; text-decoration: line-through; background-color: #fce8e8; padding: 2px 4px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. פונקציות ליבה (AI & Search)
# ==========================================

def extract_pdf_text(file):
    try:
        reader = PyPDF2.PdfReader(file)
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    except:
        return ""


def google_search_jobs(query):
    """חיפוש משרות חי באמצעות Google Custom Search API"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': search_id,
        'num': 5  # מביא את 5 התוצאות הראשונות
    }
    try:
        response = requests.get(url, params=params, timeout=20)
        return response.json().get('items', [])
    except Exception as e:
        st.error(f"שגיאת חיפוש: {e}")
        return []


def get_ai_response(prompt: str, is_json: bool = False):
    """גרסת v1 היציבה לעקיפת חסימות נטפרי"""
    if not api_key: return "שגיאה: חסר מפתח API"
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    params = {'key': api_key}
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    if is_json:
        payload["generationConfig"] = {"response_mime_type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=payload, params=params, timeout=30)
        if response.status_code != 200:
            return f"שגיאה {response.status_code}: {response.text}"
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"שגיאה בחיבור: {str(e)}"


# ==========================================
# 3. ניהול מצב האפליקציה (Session State)
# ==========================================
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "job_desc" not in st.session_state: st.session_state.job_desc = ""
if "search_results" not in st.session_state: st.session_state.search_results = []

# ==========================================
# 4. סרגל צדי (העלאת קבצים)
# ==========================================
with st.sidebar:
    st.title("⚙️ הגדרות")
    if api_key and search_id:
        st.success("מפתחות API זוהו ✅")

    st.divider()
    st.subheader("📄 שלב 1: העלאת קורות חיים")
    pdf_file = st.file_uploader("בחרי קובץ PDF", type=['pdf'])
    if pdf_file:
        with st.spinner("מחלץ טקסט..."):
            st.session_state.cv_text = extract_pdf_text(pdf_file)
            st.success("קורות החיים נטענו!")

# ==========================================
# 5. ממשק ראשי
# ==========================================
st.title("🎯 AI Career Optimizer Pro")
st.caption("חיפוש משרות חי, ניתוח התאמה ושכתוב אוטומטי")

if not st.session_state.cv_text:
    st.info("👈 התחילי בהעלאת קורות חיים בסרגל הצדי.")
    st.stop()

# --- שלב החיפוש (Live Search) ---
st.subheader("🔍 שלב 2: מציאת משרה")
col1, col2 = st.columns([3, 1])
search_query = col1.text_input("איזו משרה נחפש?", placeholder="למשל: מנהלת משרד תל אביב")
search_linkedin = st.checkbox("חפשי רק בלינקדאין (לתוצאות מסודרות)", value=True)

if col2.button("🔎 חפשי משרות"):
    with st.spinner("סורק את הרשת..."):
        final_q = f"{search_query} site:linkedin.com/jobs" if search_linkedin else f"{search_query} משרות דרושים"
        st.session_state.search_results = google_search_jobs(final_q)

# הצגת תוצאות חיפוש
if st.session_state.search_results:
    st.write("תוצאות שמצאתי עבורך:")
    for item in st.session_state.search_results:
        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <h4 style="margin:0;"><a href="{item['link']}" target="_blank">{item['title']}</a></h4>
                <p style="font-size:0.9em; color:#666; margin-top:5px;">{item['snippet']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("בצעי ניתוח למשרה זו", key=item['link']):
                st.session_state.job_desc = item['snippet']
                st.success("תיאור המשרה הוזן למערכת הניתוח!")

st.divider()

# --- שלב הניתוח והאופטימיזציה ---
st.subheader("📊 שלב 3: ניתוח ואופטימיזציה")
job_input = st.text_area("תיאור המשרה לניתוח (הוזן אוטומטית או הדביקי כאן):",
                         value=st.session_state.job_desc, height=150)

if st.button("⚡ הרץ ניתוח עמוק"):
    if not job_input:
        st.error("אנא בחרי משרה מהחיפוש או הדביקי תיאור משרה.")
    else:
        with st.spinner("ה-AI מנתח התאמה..."):
            # ניתוח מדדים
            analysis_prompt = f"Analyze CV: {st.session_state.cv_text} vs Job: {job_input}. Return ONLY JSON: {{'score': 0-100, 'missing_skills': [], 'action_plan': 'Hebrew advice'}}"
            analysis_res = get_ai_response(analysis_prompt, is_json=True)

            # שכתוב
            opt_prompt = f"Rewrite CV sections to match Job: {job_input}. Use <span class='cv-add'>text</span> for additions. Language: Hebrew. CV: {st.session_state.cv_text}"
            optimized_cv = get_ai_response(opt_prompt)

            try:
                res = json.loads(analysis_res)
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(
                        f'<div class="metric-card"><p>ציון התאמה</p><p class="metric-value">{res["score"]}%</p></div>',
                        unsafe_allow_html=True)
                with c2:
                    st.write("**📝 תוכנית פעולה:**")
                    st.write(res['action_plan'])

                st.subheader("🔍 מילות מפתח חסרות")
                st.markdown(" ".join([f'<span class="keyword-tag">{kw}</span>' for kw in res['missing_skills']]),
                            unsafe_allow_html=True)

                st.divider()
                st.subheader("📝 הצעה לשכתוב אופטימלי")
                st.markdown(
                    f'<div style="background:white; padding:25px; border:1px solid #ddd; border-radius:10px;">{optimized_cv}</div>',
                    unsafe_allow_html=True)
            except Exception as e:
                st.error("חלה שגיאה בעיבוד הנתונים. ודאי שנטפרי מאפשרים את התשובה.")