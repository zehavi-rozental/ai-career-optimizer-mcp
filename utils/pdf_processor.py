import PyPDF2
from docx import Document

def extract_text_from_pdf(pdf_file):
    """חילוץ טקסט מקובץ PDF"""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        return text if text.strip() else "לא ניתן היה לחלץ טקסט מ-PDF"
    except Exception as e:
        return f"שגיאה בקריאת PDF: {str(e)}"

def extract_text_from_docx(docx_file):
    """חילוץ טקסט מקובץ Word"""
    try:
        doc = Document(docx_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
        return text if text.strip() else "לא ניתן היה לחלץ טקסט מה-Word"
    except Exception as e:
        return f"שגיאה בקריאת Word: {str(e)}"
