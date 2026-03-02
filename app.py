import streamlit as st
import requests
import json
import PyPDF2

# ==========================================
# 1. הגדרות דף ועיצוב (UI)
# ==========================================
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# משיכת מפתחות מה-Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
search_id = st.secrets.get("SEARCH_ENGINE_ID")

# עיצוב CSS משודרג למראה מקצועי
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #ff4b4b; color: white; border: none; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #ff3333; transform: translateY(-2px); }
    .job-card {
        background: white; padding: 20px; border-radius: 12px; border: 1px solid #eee; 
        margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .metric-card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; border: 1px solid #eee;
    }
    .keyword-tag {
        display: inline-block; padding: 5px 12px; margin: 4px; border-radius: 20px;
        background-color: #ffeaea; color: #ff4b4b; font-weight: 600; border: 1px solid #ffcccc;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. פונקציות ליבה (Search & AI)
# ==========================================

def google_search_jobs(query):
    """חיפוש משרות ממוקד (עוקף שגיאת 403)"""
    if not query: return []
    url = "https://www.googleapis.com/customsearch/v1"
    # הערה: השאילתה נקייה כי הגדרת את האתרים בתוך ה-Control Panel של גוגל
    params = {'q': query, 'key': api_key, 'cx': search_id, 'num': 5}
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            return response.json().get('items', [])
        elif response.status_code == 403:
            st.error(
                "🚨 שגיאת הרשאה 403: ודאי שהגדרת אתרים ספציפיים (כמו לינקדאין) בלוח הבקרה של גוגל ומחקת את google.com.")
        else:
            st.error(f"שגיאת גוגל {response.status_code}")
    except Exception as e:
        st.error(f"שגיאת תקשורת: {e}")
    return []


def get_ai_analysis(cv_text, job_desc):
    """ניתוח עמוק באמצעות Gemini 1.5 Flash"""
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    prompt = f"""
    Analyze the following CV against the Job Description. 
    Return ONLY a JSON object with these keys: 
    'score' (0-100), 'missing_skills' (list), 'action_plan' (Hebrew text).

    CV: {cv_text[:3000]}
    JD: {job_desc}
    """
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }
    try:
        res = requests.post(url, json=payload, params={'key': api_key}, timeout=30)
        return json.loads(res.json()['candidates'][0]['content']['parts'][0]['text'])
    except:
        return None


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
    st.title("⚙️ הגדרות מערכת")
    pdf_file = st.file_uploader("📄 שלב 1: העלאת קורות חיים", type=['pdf'])
    if pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        st.session_state.cv_text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        st.success("קורות החיים נטענו בהצלחה!")

st.title("🎯 AI Career Optimizer Pro")

if not st.session_state.cv_text:
    st.info("👈 התחילי בהעלאת קורות חיים בסרגל הצדי כדי להתחיל בתהליך.")
    st.stop()

# --- שלב החיפוש ---
st.subheader("🔍 שלב 2: מציאת משרה")
col1, col2 = st.columns([3, 1])
query = col1.text_input("איזו משרה נחפש עבורך היום?", placeholder="למשל: מנהלת משרד, גיוס, אדמיניסטרציה...")

if col2.button("🔎 חפשי משרות"):
    with st.spinner("סורק אתרי דרושים נבחרים..."):
        st.session_state.search_results = google_search_jobs(query)

if st.session_state.search_results:
    for i, item in enumerate(st.session_state.search_results):
        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <h4 style="margin:0;"><a href="{item['link']}" target="_blank">{item['title']}</a></h4>
                <p style="font-size:0.9em; color:#555; margin-top:5px;">{item['snippet']}</p>
            </div>
            """, unsafe_allow_html=True)
            # שימוש ב-key ייחודי לכל כפתור למניעת שגיאות Streamlit
            if st.button(f"בצעי ניתוח למשרה #{i + 1}", key=f"select_{i}"):
                st.session_state.job_desc = item['snippet']
                st.success("פרטי המשרה הועברו לניתוח! גללי למטה.")

st.divider()

# --- שלב הניתוח ---
st.subheader("📊 שלב 3: ניתוח התאמה ואופטימיזציה")
job_input = st.text_area("תיאור המשרה (הוזן אוטומטית או הדביקי כאן):",
                         value=st.session_state.job_desc, height=150)

if st.button("⚡ הרץ ניתוח ATS עמוק"):
    if not job_input:
        st.error("אנא בחרי משרה מהחיפוש או הדביקי תיאור משרה קודם.")
    else:
        with st.spinner("ה-AI משווה נתונים ומזהה פערים..."):
            res = get_ai_analysis(st.session_state.cv_text, job_input)
            if res:
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <p style="color: #666; margin-bottom: 5px;">ציון התאמה</p>
                        <p style="font-size: 3rem; font-weight: 800; color: #ff4b4b; margin: 0;">{res['score']}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.write("**📝 תוכנית פעולה לשדרוג:**")
                    st.write(res['action_plan'])

                st.write("**🔍 מילות מפתח שחסרות לך (כדאי להוסיף):**")
                st.markdown(" ".join([f'<span class="keyword-tag">{kw}</span>' for kw in res['missing_skills']]),
                            unsafe_allow_html=True)
            else:
                st.error("לא הצלחנו לקבל ניתוח כרגע. נסי שוב בעוד רגע.")