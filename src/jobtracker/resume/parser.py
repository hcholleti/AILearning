import os
from typing import Dict, List
import spacy
import pdfplumber
from collections import Counter

nlp = spacy.load("en_core_web_sm")

# Simple skill/tech extraction from resume PDF (extend as needed)
def resume_parser(resume_path: str) -> Dict:
    text = ""
    if resume_path.lower().endswith(".pdf"):
        with pdfplumber.open(resume_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    # Add DOCX support if needed
    doc = nlp(text)
    tokens = [t.text.lower() for t in doc if t.is_alpha and not t.is_stop]
    skills = [ent.text for ent in doc.ents if ent.label_ in ("ORG", "PRODUCT", "SKILL")]
    # Most common tokens as fallback
    common = [w for w, _ in Counter(tokens).most_common(20)]
    return {
        "text": text,
        "skills": list(set(skills + common)),
        "tokens": tokens,
    }
