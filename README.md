# 🎯 AI Career Optimizer Pro

**Transform Your Career Path with Intelligent Job Matching & AI-Powered Analysis**

---

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## 🌟 Overview

**AI Career Optimizer Pro** is an intelligent career development assistant that helps professionals find job opportunities tailored to their qualifications and experience. The application combines **resume analysis**, **real-time job search**, and **AI-powered job matching** to provide personalized career recommendations.

### Problem It Solves
- 🚀 **Time-consuming job hunting**: Automatically searches relevant positions
- 📊 **Poor job-resume alignment**: Uses AI to calculate match scores
- 📈 **Lack of insights**: Provides detailed analysis of strengths, gaps, and improvement areas
- 📄 **Document management**: Seamlessly handles multiple resume formats

---

## ✨ Key Features

✅ **Resume Upload & Processing**
   - Support for PDF and DOCX formats
   - Intelligent text extraction and parsing

✅ **Real-Time Job Search**
   - Integration with Google Search API (via Serper)
   - Filtered, relevant job listings
   - Pagination for easy browsing

✅ **AI-Powered Job Matching**
   - Google Generative AI (Gemini) analysis
   - Match score calculation based on skills and keywords
   - Detailed insights: strengths, gaps, and recommendations

✅ **Interactive Dashboard**
   - Clean, user-friendly Streamlit interface
   - Session state management
   - Export capabilities (download analysis as Word document)

✅ **Multi-Language Support**
   - Hebrew and English interface
   - Supports searching jobs in multiple regions

✅ **Robust Error Handling**
   - SSL/TLS configuration for network compatibility
   - Dynamic model detection for API resilience
   - Comprehensive error messages

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Frontend** | Streamlit 1.0+ |
| **Backend** | Python 3.8+ |
| **AI & ML** | Google Generative AI (Gemini 1.5) |
| **Search** | Serper API (Google Search) |
| **Document Processing** | PyPDF2, python-docx |
| **Data Processing** | Pandas |
| **HTTP Requests** | Requests |
| **SSL/Security** | Certifi |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- API keys for:
  - 🔑 Google Generative AI (Gemini)
  - 🔑 Serper API (Google Search)

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/zehavi-rozental/ai-career-optimizer-mcp.git
cd ai-career-optimizer-mcp
```

#### 2. Create a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Verify Installation
```bash
python check_syntax.py
```

---

## ⚙️ Configuration

### API Keys Setup

Create a Streamlit secrets file at `~/.streamlit/secrets.toml`:

```toml
# Google Generative AI (Gemini) - https://ai.google.dev/
GEMINI_API_KEY = "your-gemini-api-key-here"

# Serper API (Google Search) - https://serper.dev/
SERPER_API_KEY = "your-serper-api-key-here"

# Google Custom Search (if using alternative search)
GOOGLE_API_KEY = "your-google-api-key-here"
SEARCH_ENGINE_ID = "your-custom-search-engine-id"
```

### Environment Variables (Optional)

For advanced configuration, you can set these in your `.env` file:

```bash
# Network configuration
PYTHONHTTPSVERIFY=0
GOOGLE_API_USE_MTLS=never

# API Configuration
API_TIMEOUT=20
```

### How to Get API Keys

1. **Google Generative AI (Gemini)**
   - Visit https://ai.google.dev/
   - Create a new API key
   - Enable the Generative Language API

2. **Serper API**
   - Visit https://serper.dev/
   - Sign up for free tier
   - Copy your API key from the dashboard

---

## 🚀 Usage

### Running the Application

#### Option 1: Using Streamlit Directly
```bash
streamlit run app.py
```

#### Option 2: Using the Batch Script (Windows)
```bash
run.bat
```

The application will open in your default browser at `http://localhost:8501`

### Application Workflow

#### Step 1️⃣: Upload Your Resume
- Click on the file uploader
- Select your resume (PDF or DOCX format)
- Wait for the system to extract and parse the text

#### Step 2️⃣: Search for Jobs
- Enter the job title or position type
- Click "Search" button
- Browse through the results

#### Step 3️⃣: Analyze Job Matches
- Click on a job listing to expand details
- View match score and analysis
- Read AI-powered recommendations

#### Step 4️⃣: Export Results
- Download your analysis as a Word document
- Share insights with mentors or recruiters

### Example Search Queries
```
Python Developer
Senior Data Scientist
Product Manager
Full-Stack Engineer
UX/UI Designer
```

---

## 📁 Project Structure

```
ai-career-optimizer-mcp/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── run.bat                         # Windows batch script to run the app
│
├── services/                       # Core business logic
│   ├── __init__.py
│   ├── ai_service.py              # Google Generative AI integration
│   └── google_search.py            # Serper API integration for job search
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── pdf_processor.py            # PDF text extraction
│   └── docx_generator.py           # Word document generation
│
├── assets/                         # Static files
│   └── style.css                   # Custom Streamlit styling
│
├── tests/                          # Testing utilities
│   ├── check_syntax.py             # Python syntax validation
│   ├── validate.py                 # Configuration validation
│   ├── full_test.py                # Integration tests
│   ├── test_api_direct.py          # Direct API testing
│   └── test_simple.py              # Simple functionality tests
│
└── documentation/
    ├── README.md                   # This file
    ├── SETUP_AND_DEPLOY.md         # Deployment guide
    └── NETWORK_ISSUE.md            # Network troubleshooting
```

### Key directories explained:

- **`services/`** - Contains external API integrations and business logic
  - `ai_service.py`: Handles Gemini AI analysis with robust error handling
  - `google_search.py`: Interfaces with Serper API for job search and scoring

- **`utils/`** - Utility functions for document processing
  - `pdf_processor.py`: Extracts text from PDF and DOCX files
  - `docx_generator.py`: Generates and exports Word documents with analysis

- **`assets/`** - Styling and media
  - `style.css`: Custom CSS for Streamlit UI enhancements

---

## 🔧 Validation & Testing

### Running Syntax Check
```bash
python check_syntax.py
```
Validates Python syntax across all files.

### Running Validation Tests
```bash
python validate.py
```
Checks API configuration and connectivity.

### Running Full Integration Tests
```bash
python full_test.py
```
Tests all components working together.

### Direct API Testing
```bash
python test_api_direct.py
```
Tests API connectivity without UI.

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named X"
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: SSL Certificate Error
**Solution:** The application has built-in SSL bypasses. If issues persist:
```bash
# Install certificate bundle
pip install --upgrade certifi

# Run the fix script
python fix_ssl.py
```

### Issue: API Keys Not Loading
**Solution:**
1. Verify `~/.streamlit/secrets.toml` exists
2. Check API key format (no extra quotes)
3. Ensure Streamlit is reading secrets: `streamlit config show`
4. Restart the Streamlit server

### Issue: "No Models Available" Error
**Solution:**
- Verify your Gemini API key is valid
- Check enabled APIs in Google Cloud Console
- Try alternative models (gemini-pro, gemini-1.5-pro)

### Issue: Network Connectivity Problems
**Reference:** See [NETWORK_ISSUE.md](NETWORK_ISSUE.md) for network troubleshooting.

---

## 📊 Performance & Limits

| Metric | Value |
|--------|-------|
| Max Resume Size | 100 MB |
| Job Results per Page | 10-15 |
| Average Search Time | 3-5 seconds |
| API Timeout | 20 seconds |
| Supported Resume Formats | PDF, DOCX |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙋 Support & Questions

For issues, questions, or feature requests:
- 📧 Open an issue on GitHub
- 💬 Start a discussion
- 📖 Check existing documentation

---

## 🎓 Built With ❤️ for Career Development

**AI Career Optimizer Pro** - Empowering professionals to find their perfect next opportunity.

---

**Last Updated:** April 18, 2026  
**Version:** 1.0.0