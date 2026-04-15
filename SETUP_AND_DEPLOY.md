# 🚀 AI Career Optimizer - Setup & Deploy to GitHub

## ✅ תיקונים שבוצעו

### 1. **Fixed Import Errors**
- ✅ `utils/pdf_processor.py`: עדכון לפונקציות `extract_text_from_pdf()` ו-`extract_text_from_docx()`
- ✅ `app.py`: עדכון ה-imports מ-`PDFProcessor` למציאות - כעת משתמש בפונקציות ישירות

### 2. **Fixed PDF & DOCX Upload**
- ✅ `st.file_uploader()` תומך בטעינת קבצים PDF ו-DOCX
- ✅ חילוץ טקסט רובוסטי מ-PDF וקבצי Word

### 3. **Fixed Google Search & Pagination**
- ✅ סינון דפי תוצאות כלליים (מזהה "נמצאו X משרות")
- ✅ תיאור משרה מלא עם `GoogleSearchService.get_full_job_content()` (Serper Scn- ✅ דפדוף: 10 תוצאות לעמוד, כפתורי עמוד קודם/הבא

### 4. **Fixed AI Model 404 Error**
- ✅ `AIService.get_available_model()`: בדיקה דינמית של מודלים זמינים
- ✅ ניסיון ל-`gemini-1.5-flash` קודם, אח"כ `gemini-pro`, אח"כ `gemini-1.5-pro`
- ✅ ניקוי מוחלט של מפתח API

### 5. **UI Enhancements**
- ✅ St.expander לכל משרה עם תיאור מלא
- ✅ Progress bar וציון התאמה
- ✅ כפתור הורדה ל-Word
- ✅ HTML support למילים ירוקות בניתוח

---

## 🔧 Terminal Commands to Deploy to GitHub

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Local Tests
```bash
# Test syntax
python check_syntax.py

# Run the app locally
streamlit run app.py
```

### Step 3: Commit Changes to Git
```bash
# Navigate to project folder
cd C:\Users\user\Documents\GitHub\ai-career-optimizer-mcp

# Check status
git status

# Add all changes
git add -A

# Commit with message
git commit -m "Fix: ImportError, PDF/DOCX upload, Google Search pagination, AI model 404 error, UI enhancements"

# Push to GitHub
git push origin main
```

### Step 4: Verify on GitHub
```bash
# Check log
git log --oneline -n 5

# View remote URL
git remote -v
```

---

## 📋 Files Modified

| File | Changes |
|------|---------|
| `app.py` | Complete rewrite: fixed imports, added expanders, pagination, full description loading |
| `utils/pdf_processor.py` | Added DOCX support, robust error handling |
| `services/ai_service.py` | Dynamic model detection, API key cleaning |
| `services/google_search.py` | Already had pagination & scraping (no changes needed) |
| `requirements.txt` | Added certifi, updated versions |

---

## 🚀 How to Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Streamlit secrets:** (`~/.streamlit/secrets.toml`)
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   GOOGLE_API_KEY = "your-google-api-key"
   SEARCH_ENGINE_ID = "your-search-engine-id"
   SERPER_API_KEY = "your-serper-api-key"
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Access in browser:**
   - Open: `http://localhost:8501`

---

## 🎯 Features Now Working

✅ Upload PDF/DOCX resume
✅ Search jobs with pagination (10 per page)
✅ Fetch full job descriptions from job websites
✅ Dynamic AI model detection (fixes 404 errors)
✅ Deep analysis with green keyword highlighting
✅ Download analysis as Word document
✅ Beautiful Hebrew UI with emojis

---

## 🛠️ Troubleshooting

### ImportError: No module named...
```bash
pip install -r requirements.txt --upgrade
```

### Streamlit secrets not found
- Create `~/.streamlit/secrets.toml`
- Add your API keys (see above)
- Restart streamlit

### AI Error 404/400
- The app now tries multiple models automatically
- Check your API key for hidden characters (quotes, spaces)
- Verify GEMINI_API_KEY is valid

### PDF/DOCX not extracting text
- Ensure file is not corrupted
- Try another file format
- Check console for detailed error

---

## 📝 Version History

| Date | Changes |
|------|---------|
| 2026-03-18 | Fixed ImportError, PDF/DOCX upload, pagination, AI model 404, UI enhancements |

---

**Happy Job Hunting! 🎯**

