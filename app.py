import streamlit as st
import os
import json
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from utils.docx_generator import create_improved_docx

# הגדרות דף -Layout רחב ומקצועי
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# אתחול Session State
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "search_results" not in st.session_state: st.session_state.search_results = []
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None

st.title("🎯 AI Career Optimizer Pro")
st.markdown("---")

# שלב 1: העלאת קורות חיים
with st.sidebar:
    st.header("📄 שלב 1: קורות חיים")
    pdf_file = st.file_uploader("העלי קובץ PDF", type=['pdf'])
    if pdf_file:
        with st.spinner("מחלץ טקסט..."):
            text = extract_text_from_pdf(pdf_file)
            if text:
                st.session_state.cv_text = text
                st.success("✅ הקובץ נקלט בהצלחה")

# שלב 2: לוח משרות חכם (Smart Redirect Engine)
st.subheader("🔍 שלב 2: איתור משרות חכם")
st.info("המערכת מבצעת חיפוש ממוקד (Smart Site-Search) כדי להבטיח תוצאות רלוונטיות ללא שגיאות.")

query = st.text_input("איזה תפקיד את מחפשת?", placeholder="למשל: Junior Full Stack Developer")

if st.button("חפש משרות בכל המקורות", type="primary"):
    if query:
        with st.spinner("סורק אתרים..."):
            st.session_state.search_results = GoogleSearchService.search_jobs(query)

if st.session_state.search_results:
    st.write("### בחרי מקור לחיפוש ממוקד:")
    # הגדרת אייקונים לכל אתר למראה מרשים
    icons = {"AllJobs": "💼", "GotFriends": "🤝", "Jobinfo": "📊", "Nisha": "🎯"}

    cols = st.columns(4)
    for i, item in enumerate(st.session_state.search_results):
        with cols[i % 4]:
            with st.container(border=True):
                icon = icons.get(item['source'], "🌐")
                st.markdown(f"#### {icon} {item['source']}")
                st.caption(item['desc'])
                st.link_button(f"חפש ב-{item['source']}", item['link'], use_container_width=True)

st.markdown("---")

# שלב 3: ניתוח והתאמה מבוסס AI
st.subheader("📊 שלב 3: ניתוח התאמה ושיפור (AI)")
job_input = st.text_area("הדביקי כאן את תיאור המשרה שמצאת:", height=150, placeholder="הדביקי את דרישות התפקיד...")

if st.button("🚀 נתח ושפר את קורות החיים שלי", type="primary"):
    if not job_input or not st.session_state.cv_text:
        st.warning("נא להעלות קורות חיים ולהדביק תיאור משרה.")
    else:
        with st.spinner("ה-AI מנתח את ההתאמה..."):
            # פרומפט משופר למניעת שגיאות JSON
            prompt = f"""
            Compare the CV text and Job Description. 
            CV: {st.session_state.cv_text[:2000]}
            Job: {job_input[:2000]}
            Return ONLY a valid JSON with: score (0-100), missing_skills (list), improved_sections (list of objects with 'explanation', 'original', 'improved').
            """
            res = AIService.get_response(prompt)
            if res:
                st.session_state.analysis_results = res

if st.session_state.analysis_results:
    res = st.session_state.analysis_results

    # הצגת ציון התאמה בצורה גרפית
    score = res.get('score', 0)
    st.metric("ציון התאמה למשרה", f"{score}%")
    st.progress(score / 100)

    st.write("### 📝 המלצות לשיפור")
    for section in res.get('improved_sections', []):
        with st.expander(f"💡 {section.get('explanation', '')[:60]}..."):
            st.error(f"**המקור:** {section.get('original', '')}")
            st.success(f"**ההצעה שלנו:** {section.get('improved', '')}")

    if st.button("📥 הורד קורות חיים משופרים (Word)"):
        data = create_improved_docx(st.session_state.cv_text, res.get('improved_sections', []))
        st.download_button("לחצי כאן להורדה", data, "Improved_CV.docx")