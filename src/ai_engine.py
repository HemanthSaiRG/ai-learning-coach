import os
from dotenv import load_dotenv

load_dotenv()

USE_AI = bool(os.getenv("OPENAI_API_KEY"))

if USE_AI:
    from openai import OpenAI
    from src.kb_engine import search_kb

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_learning(topic, confusions, time_spent, user_dir):
    """
    User-specific AI analysis with PDF knowledge base (RAG).
    Falls back to offline mode if API key not present.
    """

    # ---------- OFFLINE MODE ----------
    if not USE_AI:
        return {
            "topic": topic,
            "time_spent": time_spent,
            "feedback": "Offline mode: AI disabled (no API key).",
            "confusion_tip": "PDF content saved. Enable AI to use smart tutor."
        }

    # ---------- RAG CONTEXT ----------
    kb_context = search_kb(topic + " " + confusions, user_dir)

    prompt = f"""
You are a professional AI tutor.

Answer ONLY using the content below.
If answer not found, say "Not in uploaded material".

CONTENT:
{kb_context}

STUDENT TOPIC:
{topic}

CONFUSIONS:
{confusions}

TIME:
{time_spent} minutes

TASKS:
1. Explain topic simply
2. Clear confusions using content
3. Identify weak parts
4. Suggest next topics from syllabus
5. Give a short study plan
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
