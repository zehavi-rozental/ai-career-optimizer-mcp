import PyPDF2

def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        return text
    except Exception:
        return ""