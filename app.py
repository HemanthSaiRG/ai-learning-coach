import streamlit as st
import json
import os
from datetime import date
import openai

# =====================================================
# CONFIG
# =====================================================
DATA_FILE = "data/progress.json"

SYLLABUS = [
    "Arrays", "Strings", "Recursion", "Sorting", "Searching", "Linked List"
]

PRACTICE = {
    "Arrays": ["Reverse array", "Find max element", "Two sum"],
    "Strings": ["Reverse string", "Check palindrome", "Char frequency"],
    "Recursion": ["Factorial", "Fibonacci", "Sum of digits"],
    "Sorting": ["Bubble sort", "Selection sort", "Insertion sort"],
    "Searching": ["Linear search", "Binary search", "First occurrence"],
    "Linked List": ["Insert node", "Delete node", "Reverse list"]
}

# =====================================================
# SAFE STORAGE
# =====================================================
def load_progress():
    if not os.path.exists(DATA_FILE):
        return {
            "history": [],
            "current_index": 0,
            "today_done": False,
            "streak": 0,
            "last_date": ""
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_progress(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

progress = load_progress()

# daily reset
if progress["last_date"] != str(date.today()):
    progress["today_done"] = False
    progress["last_date"] = str(date.today())
    save_progress(progress)

# =====================================================
# HYBRID AI ENGINE
# =====================================================
OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))

def local_ai(topic, minutes):
    return f"""
### 📘 Study Guide (Local AI)

**Topic:** {topic}

1. Revise basic definition
2. Understand examples
3. Write code by hand
4. Solve practice questions

⏱ {minutes} minutes is enough.

You are on the right track.
"""

def real_ai(topic, minutes):
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = f"""
Explain {topic} simply for a student.
Suggest what to do in {minutes} minutes.
"""
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content
    except:
        return local_ai(topic, minutes)

def analyze(topic, minutes):
    if OPENAI_AVAILABLE:
        return real_ai(topic, minutes)
    return local_ai(topic, minutes)

# =====================================================
# UI
# =====================================================
st.set_page_config("AI Learning Coach", layout="centered")
st.caption("AI Learning Coach • Hybrid Mode • Stable")

page = st.sidebar.radio("Navigate", [
    "Today", "Study", "Practice", "History", "About"
])

current_topic = SYLLABUS[progress["current_index"]]

# =====================================================
# TODAY
# =====================================================
if page == "Today":
    st.header("🌱 Today")

    if progress["today_done"]:
        st.success("You’re done for today. See you tomorrow 🌙")
        st.write(f"Next topic: **{current_topic}**")
    else:
        st.markdown(f"""
### 🎯 Today’s focus
**{current_topic}**

⏱ 30 minutes is enough.
""")
        if st.button("Start"):
            st.session_state.page = "Study"
            st.rerun()

# =====================================================
# STUDY
# =====================================================
elif page == "Study":
    st.header("📘 Study")

    st.write(f"Topic: **{current_topic}**")
    minutes = st.slider("Time spent", 10, 60, 30)

    if st.button("Analyze"):
        st.info(analyze(current_topic, minutes))
        progress["study_minutes"] = minutes
        save_progress(progress)

    if st.button("Finish study"):
        st.success("Study done. Go to practice 👇")

# =====================================================
# PRACTICE
# =====================================================
elif page == "Practice":
    st.header("🧩 Practice")

    questions = PRACTICE[current_topic]
    completed = []

    for q in questions:
        completed.append(st.checkbox(q))

    if all(completed):
        st.success("Practice complete 🎉")

        progress["today_done"] = True
        progress["streak"] += 1
        progress["history"].append({
            "date": str(date.today()),
            "topic": current_topic,
            "minutes": progress.get("study_minutes", 0)
        })

        progress["current_index"] = min(
            progress["current_index"] + 1,
            len(SYLLABUS) - 1
        )

        save_progress(progress)
        st.info("You’re done for today. See you tomorrow 🌱")

# =====================================================
# HISTORY
# =====================================================
elif page == "History":
    st.header("📚 History")

    if not progress["history"]:
        st.info("No history yet")
    else:
        for h in reversed(progress["history"]):
            st.write(f"- {h['date']} • {h['topic']} • {h['minutes']} min")

# =====================================================
# ABOUT
# =====================================================
elif page == "About":
    st.markdown("""
# 🎓 AI Learning Coach

A **simple daily study guide for students who feel stuck**.

This app:
- guides you daily
- removes decision fatigue
- gives closure
- remembers progress
- works offline
- works without API
- works on mobile
- upgrades automatically when AI is available

Built with ❤️ by Hemanth.
""")
