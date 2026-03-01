import streamlit as st
import requests
import json
import PyPDF2
from datetime import datetime

# ==========================================
# 1. PAGE CONFIG & UI THEME
# ==========================================
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# משיכת המפתח מה-Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

# עיצוב CSS משודרג - נשמר לטובת המראה המקצועי
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #ff4b4b; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #ff3333; border: none; }
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #eee;
    }
    .metric-value { font-size: 3.5rem; font-weight: 800; color: #ff4b4b; margin: 0; }
    .keyword-tag {
        display: inline-block;
        padding: 5px 12px;
        margin: 4px;
        border-radius: 20px;
        background-color: #ffeaea;
        color: #ff4b4b;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid #ffcccc;
    }
    .cv-add { color: #28a745; font-weight: bold; background-color: #e6ffed; padding: 2px 4px; border-radius: 4px; }
    .cv-del { color: #dc3545; text-decoration: line-through; background-color: #fce8e8; padding: 2px 4px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. CORE FUNCTIONS (REST API VERSION)
# ==========================================

def extract_pdf_text(file) -> str:
    """מחלץ טקסט מ-PDF בצורה אמינה"""
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def get_ai_response(prompt: str, is_json: bool = False):
    """
    פונקציה המשתמשת ב-REST API כדי לעקוף חסימות ספריות של נטפרי.
    זוהי הדרך המקצועית ביותר לתקשורת עם AI בסביבה מסוננת.
    """
    if not api_key:
        return None

    # כתובת ה-API הישירה - נטפרי פותחים כתובות כאלו
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    headers = {'Content-Type': 'application/json'}

    # בניית המבנה הנדרש על ידי גוגל באופן ידני
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    if is_json:
        payload["generationConfig"] = {"response_mime_type": "application/json"}

    try:
        # שימוש ב-requests.post שהיא פקודה סטנדרטית
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()

        # חילוץ הטקסט מהמבנה המורכב של התשובה
        return result['candidates'][0]['content']['parts'][0]['text']

    except Exception as e:
        return f"ERROR_CONNECTION: {str(e)}"


# ==========================================
# 3. SIDEBAR - SETTINGS & CV UPLOAD
# ==========================================

if "cv_text" not in st.session_state:
    st.session_state.cv_text = ""
if "job_history" not in st.session_state:
    st.session_state.job_history = []

with st.sidebar:
    st.title("⚙️ הגדרות מערכת")

    if api_key:
        st.success("מפתח API זוהה ב-Secrets ✅")
    else:
        api_key = st.text_input("הזן מפתח Google API", type="password")

    st.divider()
    st.subheader("📄 קורות חיים")
    upload_method = st.radio("שיטת הזנה", ["העלאת קובץ PDF", "הדבקת טקסט"])

    if upload_method == "העלאת קובץ PDF":
        pdf_file = st.file_uploader("בחר קובץ PDF", type=['pdf'])
        if pdf_file:
            with st.spinner("מחלץ טקסט מתוך ה-PDF..."):
                text = extract_pdf_text(pdf_file)
                if text and not text.startswith("Error"):
                    st.session_state.cv_text = text
                    st.success("הקובץ נקרא בהצלחה!")
                else:
                    st.error("לא הצלחנו לקרוא את הקובץ. נסי להדביק טקסט.")
    else:
        cv_input = st.text_area("הדבקי את קורות החיים שלך כאן", height=200)
        if st.button("שמור טקסט"):
            st.session_state.cv_text = cv_input
            st.success("הטקסט נשמר!")

# ==========================================
# 4. MAIN INTERFACE
# ==========================================

st.title("🎯 AI Career Optimizer Pro")
st.caption("ניתוח חכם, זיהוי פערים ואופטימיזציה אוטומטית למערכות ATS")

if not api_key or not st.session_state.cv_text:
    st.info("👈 התחילי בהעלאת קורות חיים בסרגל הצדי כדי להתחיל.")
    st.stop()

# שלב 1: הזנת משרה
st.subheader("1. פרטי המשרה המבוקשת")
job_desc = st.text_area("הדביקי כאן את תיאור המשרה (Job Description)", height=150,
                        placeholder="העתיקי לכאן את דרישות התפקיד מלינקדאין או מכל אתר אחר...")

if st.button("⚡ הרץ ניתוח ואופטימיזציה"):
    if not job_desc:
        st.error("אנא הכניסי תיאור משרה קודם.")
    else:
        with st.spinner("ה-AI מבצע השוואה עמוקה..."):
            # פניה ל-AI לניתוח מדדים (REST API)
            analysis_prompt = f"""
            Analyze this CV against the Job Description. Return ONLY JSON:
            {{
                "score": <0-100>,
                "missing_skills": ["skill1", "skill2"],
                "present_skills": ["skill1", "skill2"],
                "action_plan": "Short strategy advice in Hebrew"
            }}
            CV: {st.session_state.cv_text}
            JD: {job_desc}
            """
            analysis_res = get_ai_response(analysis_prompt, is_json=True)

            # פניה ל-AI לאופטימיזציה של הטקסט
            optimize_prompt = f"""
            Rewrite the 'Professional Summary' and 'Experience' sections of this CV to match the JD.
            Use <span class='cv-add'>text</span> for additions and <span class='cv-del'>text</span> for deletions.
            Language: Hebrew.
            CV: {st.session_state.cv_text}
            JD: {job_desc}
            """
            optimized_cv = get_ai_response(optimize_prompt)

            if "ERROR_CONNECTION" in analysis_res:
                st.error(f"שגיאת תקשורת: {analysis_res}. ודאי שנטפרי פתחו את הכתובת.")
            else:
                try:
                    res = json.loads(analysis_res)

                    # תצוגת תוצאות ויזואלית
                    st.divider()
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <p style="color: #666; margin-bottom: 5px;">ציון התאמה ATS</p>
                            <p class="metric-value">{res['score']}%</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.subheader("📝 תוכנית פעולה")
                        st.write(res['action_plan'])

                    # ענן מילות מפתח חסרות
                    st.subheader("🔍 מילות מפתח שחסרות בקורות החיים שלך")
                    kw_html = "".join([f'<span class="keyword-tag">{kw}</span>' for kw in res['missing_skills']])
                    st.markdown(kw_html, unsafe_allow_html=True)

                    # תצוגת קורות החיים המעודכנים
                    st.divider()
                    st.subheader("📝 הצעה לשכתוב אופטימלי")
                    st.caption("השינויים המסומנים יעזרו לך לעבור את סינון ה-ATS:")
                    st.markdown(
                        f'<div style="background: white; padding: 25px; border-radius: 10px; border: 1px solid #ddd; line-height: 1.6;">{optimized_cv}</div>',
                        unsafe_allow_html=True)

                    # שמירה להיסטוריה
                    st.session_state.job_history.append(
                        {"date": datetime.now().strftime("%d/%m %H:%M"), "score": res['score']})

                except Exception as e:
                    st.error(f"שגיאה בעיבוד נתוני ה-AI: {e}")

# היסטוריה ויזואלית
if st.session_state.job_history:
    st.divider()
    st.subheader("📜 גרף שיפור ביצועים")
    scores = [x['score'] for x in st.session_state.job_history]
    st.line_chart(scores)