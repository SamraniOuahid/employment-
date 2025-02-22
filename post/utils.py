# utils.py

import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extrait le texte brut d'un fichier PDF."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""  # Gère les pages sans texte
    return text.strip()*10