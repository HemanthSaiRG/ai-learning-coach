import os
import json

def search_kb(query, user_dir):
    """
    Lightweight keyword-based KB search (NO torch, NO transformers)
    Safe for Windows + Streamlit Cloud
    """

    kb_path = os.path.join(user_dir, "pdf_kb.json")

    if not os.path.exists(kb_path):
        return "No uploaded material found."

    with open(kb_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    content = data.get("content", "")

    # Simple keyword filter (works surprisingly well)
    keywords = query.lower().split()
    lines = content.split("\n")

    matched = [
        line for line in lines
        if any(k in line.lower() for k in keywords)
    ]

    return "\n".join(matched[:50]) if matched else content[:2000]
