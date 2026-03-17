import streamlit as st
from services.ai_service import AIService
from services.google_search import GoogleSearchService
from utils.pdf_processor import extract_text_from_pdf
from utils.docx_generator import create_improved_docx

# 1. הגדרות דף
st.set_page_config(page_title="AI Career Optimizer Pro", page_icon="🎯", layout="wide")

# 2. אתחול Session State (הוספת משתנה למשרה שנבחרה)
if "cv_text" not in st.session_state: st.session_state.cv_text = ""
if "search_results" not in st.session_state: st.session_state.search_results = []
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None
if "selected_job_description" not in st.session_state: st.session_state.selected_job_description = ""

st.title("🎯 AI Career Optimizer Pro")
st.markdown("---")

# שלב 1: העלאת קורות חיים (בסרגל הצד)
with st.sidebar:
    st.header("📄 שלב 1: קורות חיים")
    pdf_file = st.file_uploader("העלי קובץ PDF", type=['pdf'])
    if pdf_file:
        with st.spinner("מחלץ טקסט..."):
            text = extract_text_from_pdf(pdf_file)
            if text:
                st.session_state.cv_text = text
                st.success("✅ קורות החיים נטענו")

# שלב 2: פיד משרות אינטראקטיבי
st.subheader("🔍 שלב 2: פיד משרות ממוקד")
query = st.text_input("איזה תפקיד את מחפשת?", placeholder="למשל: Junior Full Stack Developer")

if st.button("מצא לי משרות רלוונטיות", type="primary"):
    if query:
        with st.spinner("סורק אתרי גיוס ומאנדקס משרות..."):
            st.session_state.search_results = GoogleSearchService.search_jobs(query)

if st.session_state.search_results:
    st.write(f"### נמצאו {len(st.session_state.search_results)} משרות רלוונטיות:")

    for i, job in enumerate(st.session_state.search_results):
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader(job['title'])
                st.caption(f"📍 מקור: {job['display_link']}")
                st.write(job['snippet'])
            with col2:
                # כפתור הקסם: מעביר את תוכן המשרה לשלב הבא
                if st.button("בחר לניתוח 🎯", key=f"btn_{i}"):
                    st.session_state.selected_job_description = job['snippet']
                    st.toast("המשרה נטענה בהצלחה לשלב 3!")
                st.link_button("למשרה המלאה 🔗", job['link'])

st.markdown("---")

# שלב 3: ניתוח והתאמה
st.subheader("📊 שלב 3: ניתוח התאמה ושיפור (AI)")

# תיבת הטקסט מקבלת אוטומטית את הערך שנבחר בשלב 2
job_input = st.text_area(
    "תיאור המשרה לניתוח:",
    value=st.session_state.selected_job_description,
    height=150,
    placeholder="תיאור המשרה יופיע כאן אוטומטית לאחר שתבחרי משרה למעלה..."
)

if st.button("🚀 נתח ושפר את קורות החיים שלי", type="primary"):
    if not job_input or not st.session_state.cv_text:
        st.warning("נא לוודא שיש קורות חיים ותיאור משרה.")
    else:
        with st.spinner("ה-AI מנתח התאמה ומכין המלצות..."):
            prompt = f"Compare CV and Job. Return JSON only. CV: {st.session_state.cv_text[:2000]} Job: {job_input[:2000]}"
            res = AIService.get_response(prompt)
            if res:
                st.session_state.analysis_results = res

if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    st.metric("ציון התאמה", f"{res.get('score', 0)}%")

    st.write("### 📝 המלצות שיפור ספציפיות")
    for section in res.get('improved_sections', []):
        with st.expander(f"💡 {section.get('explanation', '')[:60]}..."):
            st.error(f"**במקור:** {section.get('original', '')}")
            st.success(f"**ההצעה שלנו:** {section.get('improved', '')}")

    if st.button("📥 הורד קורות חיים משופרים (Word)"):
        data = create_improved_docx(st.session_state.cv_text, res.get('improved_sections', []))
        st.download_button("לחצי כאן להורדה", data, "Improved_CV.docx")