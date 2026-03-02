from docx import Document
from docx.shared import RGBColor
import io


def create_improved_docx(diff_data):
    doc = Document()
    doc.add_heading('Improved CV - AI Career Optimizer', 0)

    doc.add_heading('Explanation of Changes:', level=1)
    doc.add_paragraph(diff_data.get('explanation', 'Optimized for target job description.'))

    doc.add_heading('Revised CV (Marked Version):', level=1)
    p = doc.add_paragraph()

    for part, status in diff_data.get('diff', []):
        run = p.add_run(part)
        if status == 'add':
            run.font.color.rgb = RGBColor(0, 128, 0)  # Green for additions
            run.bold = True
        elif status == 'remove':
            run.font.color.rgb = RGBColor(255, 0, 0)  # Red for deletions
            run.font.strike = True

    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio