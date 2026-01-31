from pypdf import PdfReader
import os
import json

def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def build_kb(file, user_dir):
    """
    Build a knowledge base from uploaded PDF
    and save it inside user's workspace
    """
    text = extract_text(file)

    kb_path = os.path.join(user_dir, "pdf_kb.json")
    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "source": file.name,
                "content": text
            },
            f,
            indent=2
        )

    return text
