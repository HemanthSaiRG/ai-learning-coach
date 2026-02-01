import streamlit as st
import json
from datetime import date

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
    "Recursion": ["Factorial", "Fibonacci", "Sum of digits"]
}

# =====================================================
# STORAGE (SAFE)
# =====================================================
def load_progress():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "history": [],
            "today_done": False,
            "current_index": 0,
            "streak": 0
        }

def save_progress(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

progress = load_progress()

# reset daily
if progress.get("last_date") != str(date.today()):
    progress["today_done"] = False
    progress["last_date"] = str(date.today())
    save_progress(progress)

# =====================================================
# UI
# =====================================================
st.set_page_config("AI Learning Coach", layout="centered")
st.caption("AI Learning Coach • v1.0 • Stable")

page = st.sidebar.radio("Navigate", [
    "Today", "Study", "Practice", "History", "About"
])

current_topic = SYLLABUS[progress["current_index"]]

# =====================================================
# TODAY PAGE
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
        if st.button("Start study"):
            st.session_state.page = "Study"
            st.experimental_rerun()

# =====================================================
# STUDY PAGE
# =====================================================
elif page == "Study":
    st.header("📘 Study")

    st.write(f"Topic: **{current_topic}**")
    minutes = st.slider("Time spent", 10, 60, 30)

    if st.button("Finish study"):
        progress["study_minutes"] = minutes
        save_progress(progress)
        st.success("Study done. Now practice 👇")

# =====================================================
# PRACTICE PAGE
# =====================================================
elif page == "Practice":
    st.header("🧩 Practice")

    questions = PRACTICE.get(current_topic, [])

    completed = []
    for q in questions:
        completed.append(st.checkbox(q))

    if questions and all(completed):
        st.success("Practice complete 🎉")

        # mark day complete
        progress["today_done"] = True
        progress["streak"] += 1

        progress["history"].append({
            "date": str(date.today()),
            "topic": current_topic,
            "minutes": progress.get("study_minutes", 0)
        })

        progress["current_index"] += 1
        save_progress(progress)

        st.info("You’re done for today. See you tomorrow 🌱")

# =====================================================
# HISTORY PAGE
# =====================================================
elif page == "History":
    st.header("📚 History")

    if not progress["history"]:
        st.info("No history yet")
    else:
        for h in reversed(progress["history"]):
            st.write(f"- {h['date']} • {h['topic']} • {h['minutes']} min")

# =====================================================
# ABOUT PAGE
# =====================================================
elif page == "About":
    st.markdown("""
# 🎓 AI Learning Coach

A **simple daily study guide for students who feel stuck**.

This app:
- removes decision fatigue
- guides you one step at a time
- remembers your progress
- gives closure
- helps you come back tomorrow

Built with ❤️ by Hemanth.
""")
