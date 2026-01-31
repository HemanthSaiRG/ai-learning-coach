import os
import streamlit as st
from dotenv import load_dotenv
from src.kb_engine import search_kb

load_dotenv()

def free_ai_response(topic, confusions, time_spent, kb_context):
    points = kb_context.split("\n")[:5]

    return f"""
## 📘 Topic Summary
**{topic}** is an important topic. Focus on:
- definitions
- examples
- applications
- common mistakes

## 🧩 Confusion Clearing
You mentioned: **{confusions}**  
Re-read related PDF sections and rewrite in your own words.

## ⚠️ Weak Areas
- linking concepts
- applying theory
- recall speed

## 🔜 Next Topics
- related subtopics of {topic}
- previous exam questions
- practice problems

## 🗓 Simple Study Plan
- 10 min revise
- 25 min practice
- 10 min summary
- 5 min self-test

## 📄 Reference (from uploaded material)
{chr(10).join(points)}
"""


def analyze_learning(topic, confusions, time_spent, user_dir):
    kb_context = search_kb(topic + " " + confusions, user_dir)

    demo_mode = st.session_state.get("DEMO_MODE", True)
    use_ai = bool(os.getenv("OPENAI_API_KEY")) and not demo_mode

    if demo_mode:
        return "🧪 DEMO MODE (Simulated AI)\n\n" + free_ai_response(
            topic, confusions, time_spent, kb_context
        )

    if not use_ai:
        return free_ai_response(topic, confusions, time_spent, kb_context)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
You are an AI tutor. Answer only from content below.

CONTENT:
{kb_context}

TOPIC: {topic}
CONFUSIONS: {confusions}
TIME: {time_spent} minutes

Explain clearly, clear doubts, identify weak areas, suggest next topics, and give a plan.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception:
        return free_ai_response(topic, confusions, time_spent, kb_context)
