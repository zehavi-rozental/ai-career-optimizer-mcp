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
# 2. טעינת עיצוב (Load CSS - Safe Loading)
# ==========================================
css_path = os.path.join("assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.info("Style file loading...") # הודעה שקטה במקום קריסה אם הקובץ חסר

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

# --- שלב 2: חיפוש משרות ---
st.subheader("🔍 Step 2: Find a Job")

# הצגת אזהרה אם אין CV, אבל תן למשתמש לחפש בכל זאת
if not st.session_state.cv_text:
    st.warning("⚠️ טעינת CV תשפר את הניתוח! אך באפשרותך לחפש משרות גם עכשיו.")

col1, col2 = st.columns([3, 1])
query = col1.text_input("What role are we looking for?", placeholder="e.g. מנהלת משרד", key="job_query")

if col2.button("🔎 Search Jobs"):
    if not query or query.strip() == "":
        st.error("❌ אנא הקלד כיתוב חיפוש תחת מה לחפש!")
    else:
        with st.spinner("🔄 Searching for opportunities..."):
            try:
                results = GoogleSearchService.search_jobs(query)
                if results:
                    st.session_state.search_results = results
                    st.success(f"✅ נמצאו {len(results)} משרות!")
                else:
                    st.warning("⚠️ לא נמצאו תוצאות. אנא נסה חיפוש אחר.")
                    st.session_state.search_results = []
            except Exception as e:
                st.error(f"❌ שגיאה בחיפוש: {str(e)}")
                st.session_state.search_results = []

# הצגת תוצאות
if st.session_state.search_results:
    st.markdown("### 📋 תוצאות חיפוש:")
    for i, item in enumerate(st.session_state.search_results):
        # בדיקה שהמפתחות קיימים בתוצאה
        title = item.get('title', 'ללא כותרת')
        link = item.get('link', '#')
        snippet = item.get('snippet', 'אין תיאור זמין')

        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <h4><a href="{link}" target="_blank">{title}</a></h4>
                <p>{snippet}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"📌 Analyze Job #{i+1}", key=f"select_{i}"):
                st.session_state.job_desc = snippet
                st.success("✅ Job details captured!")

st.divider()

# --- שלב 3: ניתוח התאמה ---
st.subheader("📊 Step 3: Match Analysis")
job_input = st.text_area("Job Description:", value=st.session_state.job_desc, height=150)

if st.button("⚡ Run Deep ATS Analysis"):
    if not job_input or job_input.strip() == "":
        st.error("❌ אנא הקלד תיאור משרה!")
    elif not st.session_state.cv_text:
        st.error("❌ אנא טען CV תחילה בעמודה הצדדית (בשורה 'Step 1')!")
    else:
        with st.spinner("🤖 AI is analyzing..."):
            prompt = f"CV: {st.session_state.cv_text[:3000]} Job: {job_input}. Return JSON with 'score', 'missing_skills', 'action_plan'."
            res = AIService.get_response(prompt)
            if res and isinstance(res, dict):
                try:
                    score = res.get('score', 'N/A')
                    action_plan = res.get('action_plan', 'אין תוכנית פעולה זמינה')
                    missing_skills = res.get('missing_skills', [])

                    c1, c2 = st.columns([1, 2])
                    c1.metric("Match Score", f"{score}%")
                    c2.write(f"**📋 Action Plan:** {action_plan}")
                    st.write("**🎯 Missing Keywords:**")
                    if isinstance(missing_skills, list) and missing_skills:
                        st.markdown(" ".join([f'<span class="keyword-tag">{kw}</span>' for kw in missing_skills]), unsafe_allow_html=True)
                    else:
                        st.info("✅ כל הכישורים נמצאים!")
                except Exception as e:
                    st.error(f"❌ שגיאה בעיבוד התוצאה: {str(e)}")
            else:
                st.error("❌ שגיאה בקבלת תשובה מ-AI Service")

st.divider()

# --- שלב 4: הורדת קובץ Word ---
st.subheader("📝 Step 4: Download Tailored CV")
if st.button("🪄 Generate Word Document"):
    if not job_input or job_input.strip() == "":
        st.error("❌ אנא הקלד תיאור משרה תחילה!")
    elif not st.session_state.cv_text:
        st.error("❌ אנא טען CV תחילה בעמודה הצדדית!")
    else:
        with st.spinner("✨ Creating your Word file..."):
            prompt = f"Tailor this CV to the job. CV: {st.session_state.cv_text[:3000]} Job: {job_input}. Return JSON with 'diff' (list of [text, status]) and 'explanation'."
            res = AIService.get_response(prompt)
            if res and isinstance(res, dict):
                try:
                    doc_file = create_improved_docx(res)
                    st.download_button("📥 Download Word File", data=doc_file, file_name="Tailored_CV.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                    st.success("✅ קובץ Word הוכן בהצלחה!")
                except Exception as e:
                    st.error(f"❌ שגיאה ביצירת קובץ Word: {str(e)}")
            else:
                st.error("❌ שגיאה בקבלת תשובה מ-AI Service")
