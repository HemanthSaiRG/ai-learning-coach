import os
from dotenv import load_dotenv
from src.kb_engine import search_kb

load_dotenv()

# ---------- MODES ----------
DEMO_MODE = True   # 👈 CHANGE TO False when real AI available
USE_AI = bool(os.getenv("OPENAI_API_KEY")) and not DEMO_MODE

if USE_AI:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def free_ai_response(topic, confusions, time_spent, kb_context):
    """Free rule-based AI (no API, no quota)"""
    response = f"""
### 📘 Topic Explanation
{topic} is an important concept. Based on your material, focus on understanding the definitions and examples.

### 🧩 Clearing Confusions
Your confusion: {confusions}
Re-read related sections from uploaded PDF.

### ⚠️ Weak Areas
- Definitions
- Examples
- Applications

### 🔜 What to Study Next
- Related subtopics of {topic}
- Practice questions
- Revise notes

### 🗓 Simple Study Plan
- 15 min revise
- 30 min practice
- 15 min summary
"""
    return response


def analyze_learning(topic, confusions, time_spent, user_dir):
    kb_context = search_kb(topic + " " + confusions, user_dir)

    # ---------- DEMO MODE ----------
    if DEMO_MODE:
        return (
            "🧪 DEMO MODE (AI simulated)\n\n"
            + free_ai_response(topic, confusions, time_spent, kb_context)
        )

    # ---------- FREE OFFLINE MODE ----------
    if not USE_AI:
        return free_ai_response(topic, confusions, time_spent, kb_context)

    # ---------- REAL AI MODE ----------
    try:
        prompt = f"""
You are a professional AI tutor.

Answer ONLY using the content below.

CONTENT:
{kb_context}

TOPIC:
{topic}

CONFUSIONS:
{confusions}

TIME:
{time_spent} minutes

Explain, clear doubts, find weak areas, suggest next topics, and give a plan.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception:
        return free_ai_response(topic, confusions, time_spent, kb_context)
