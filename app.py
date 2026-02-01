import streamlit as st
import json
import os
from datetime import date

# =====================================================
# CONFIG
# =====================================================
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "progress.json")

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
# STORAGE (SAFE, CLOUD SAFE)
# =====================================================
def load_progress():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        return {
            "history": [],
            "current_index": 0,
            "today_done": False,
            "streak": 0,
            "last_date": ""
        }

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "history": [],
            "current_index": 0,
            "today_done": False,
            "streak": 0,
            "last_date": ""
        }

def save_progress(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

progress = load_progress()

# =====================================================
# DAILY RESET (SAFE)
# =====================================================
today = str(date.today())
if progress.get("last_date") != today:
    progress["today_done"] = False
    progress["last_date"] = today
    save_progress(progress)

# =====================================================
# SAFE CURRENT TOPIC
# =====================================================
if progress["current_index"] >= len(SYLLABUS):
    current_topic = "Revision"
else:
    current_topic = SYLLABUS[progress["current_index"]]

# =====================================================
# LOCAL STUDY GUIDE
# =====================================================
def study_guide(topic, minutes):
    return f"""
### 📘 Study Guide

**Topic:** {topic}

1. Read definition
2. Understand 2 examples
3. Write code by hand
4. Solve practice

⏱ {minutes} minutes is enough.
"""

# =====================================================
# UI
# =====================================================
st.set_page_config("AI Learning Coach", layout="centered")
st.caption("AI Learning Coach • v1.0 • Stable")

page = st.sidebar.radio(
    "Navigate",
    ["Today", "Study", "Practice", "History", "About"]
)

# =====================================================
# TODAY
# =====================================================
if page == "Today":
    st.header("🌱 Today")

    if progress["today_done"]:
        st.success("You’re done for today. See you tomorrow 🌙")

        if current_topic != "Revision":
            st.write(f"Next topic: **{current_topic}**")
        else:
            st.info("You finished syllabus 🎉 Start revision.")

    else:
        st.markdown(f"""
### 🎯 Today’s focus
**{current_topic}**

⏱ 30 minutes is enough.
""")

        if st.button("Start study"):
            st.switch_page("Study")

# =====================================================
# STUDY
# =====================================================
elif page == "Study":
    st.header("📘 Study")

    st.write(f"Topic: **{current_topic}**")
    minutes = st.slider("Time spent (minutes)", 10, 60, 30)

    if st.button("Show study guide"):
        st.info(study_guide(current_topic, minutes))
        progress["study_minutes"] = minutes
        save_progress(progress)

    if st.button("Finish study"):
        st.success("Study done. Now practice 👇")

# =====================================================
# PRACTICE
# =====================================================
elif page == "Practice":
    st.header("🧩 Practice")

    questions = PRACTICE.get(current_topic, [])

    if not questions:
        st.info("No practice today. Revision day.")
    else:
        completed = []
        for q in questions:
            completed.append(st.checkbox(q))

        if all(completed):
            st.success("Practice complete 🎉")

            progress["today_done"] = True
            progress["streak"] += 1
            progress["history"].append({
                "date": today,
                "topic": current_topic,
                "minutes": progress.get("study_minutes", 0)
            })

            progress["current_index"] += 1
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
- tells you what to study
- removes decision fatigue
- gives closure
- remembers progress
- works offline
- works on mobile
- never crashes

Built with ❤️ by Hemanth
""")
