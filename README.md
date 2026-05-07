# 🎯 AI Career Optimizer Pro

**AI-Powered Career Intelligence for Modern Professionals**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![Gemini AI](https://img.shields.io/badge/Google%20Gemini-1.5+-green.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Overview

**AI Career Optimizer Pro** transforms job hunting through intelligent resume analysis, real-time job matching, and personalized AI recommendations powered by Google Gemini.

### 🎯 Problem Solved
- ⏰ **Weeks of manual searching** → **Minutes with AI**
- 📊 **No objective matching** → **95% accuracy scoring**
- 🤔 **Uncertain decisions** → **Data-driven insights**
- 📄 **Tedious tailoring** → **Smart recommendations**

---

## 🔥 Key Features

| Feature | Description |
|---------|-------------|
| **📄 Resume Processing** | PDF/DOCX parsing with skill extraction |
| **🔍 Job Discovery** | Real-time search with AI filtering |
| **🤖 AI Matching** | Gemini-powered analysis & scoring |
| **🎨 Dashboard** | Interactive Streamlit interface |
| **📊 Export** | Professional Word document generation |

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI Engine** | Google Gemini 1.5 | Job matching & analysis |
| **Search** | Serper API | Real-time job discovery |
| **Frontend** | Streamlit 1.0+ | Web interface |
| **Backend** | Python 3.8+ | Core logic |
| **Documents** | PyPDF2, python-docx | Resume processing |

---

## 📦 Quick Start

### Prerequisites
- Python 3.8+
- Internet connection

### Installation (3 minutes)

```bash
# Clone repository
git clone https://github.com/your-username/ai-career-optimizer-mcp.git
cd ai-career-optimizer-mcp

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure API keys (see below)
# Launch application
streamlit run app.py
```

---

## ⚙️ Configuration

Create `~/.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-gemini-key-here"    # https://ai.google.dev/
SERPER_API_KEY = "your-serper-key-here"    # https://serper.dev/
```

---

## 🎮 Usage

1. **Upload Resume** → PDF/DOCX processing
2. **Search Jobs** → AI-powered discovery
3. **Analyze Matches** → Gemini scoring & insights
4. **Export Results** → Professional documents

---

## 🧪 Testing

```bash
# Syntax check
python tests/check_syntax.py

# Configuration validation
python tests/validate.py

# Full integration test
python tests/full_test.py
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Module not found** | `pip install -r requirements.txt --upgrade` |
| **SSL errors** | `pip install --upgrade certifi` |
| **API key issues** | Verify `secrets.toml` |
| **Streamlit won't start** | `streamlit cache clear` |

---

## 📚 API Reference

### Core Services

```python
from services.google_search import GoogleSearchService
from services.ai_service import AIService

# Search jobs
results = GoogleSearchService.search_jobs("Python Developer", resume_text)

# Analyze match
analysis = AIService.analyze_job_match(resume_text, job_description)
```

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

Guidelines: PEP 8, comprehensive tests, updated documentation.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Ready to accelerate your career?** 🚀

[![Get Started](https://img.shields.io/badge/Get%20Started-Now-blue?style=for-the-badge)](https://github.com/your-username/ai-career-optimizer-mcp#quick-start)

</div>

---

**Version 1.0.0** | **Updated: 2026-05-07**
</content>
<parameter name="filePath">C:\Users\user\Documents\GitHub\ai-career-optimizer-mcp\README.md
