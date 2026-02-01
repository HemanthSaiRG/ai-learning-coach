import streamlit as st
import json
from datetime import date
from pathlib import Path

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Daily Study OS", layout="centered")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "study_log.json"

# ---------------- HELPERS ----------------
def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {
        "current_phase": None,
        "history": []
    }

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

data = load_data()

# ---------------- HEADER ----------------
st.markdown("## 📘 Daily Study OS")
st.caption("A simple daily guide for students who feel stuck")

st.divider()

# ---------------- PHASE SETUP ----------------
if not data["current_phase"]:
    st.markdown("### 🎯 Set your current learning phase")
    phase = st.text_input(
        "Example: Placement Prep, Exam Revision, Learning Something New"
    )

    if st.button("Start Phase"):
        if phase.strip():
            data["current_phase"] = phase.strip()
            save_data(data)
            st.rerun()
    st.stop()

# ---------------- PHASE BAR ----------------
col1, col2 = st.columns([3,1])
col1.markdown(f"**Current Phase:** {data['current_phase']}")
if col2.button("Change"):
    data["current_phase"] = None
    save_data(data)
    st.rerun()

st.divider()

# ---------------- STREAK ----------------
unique_days = {h["date"] for h in data["history"]}
st.markdown(f"🔥 **Streak:** {len(unique_days)} days")

st.divider()

# ---------------- TODAY ----------------
today_done = any(h["date"] == str(date.today()) for h in data["history"])

st.markdown("### 📌 Today's Focus")

if not today_done:
    topic = st.text_input("What are you studying today?")

    if st.button("Mark as Done"):
        if topic.strip():
            data["history"].append({
                "date": str(date.today()),
                "topic": topic.strip(),
                "status": "done"
            })
            save_data(data)
            st.success("You’re done for today 🌱")
            st.info("Rest well. Come back tomorrow for the next small step.")
            st.rerun()
else:
    st.success("✅ You already completed today’s study.")
    st.info("See you tomorrow 🌱")

# ---------------- HISTORY ----------------
st.divider()
st.markdown("### 📅 Recent History")

if data["history"]:
    for item in reversed(data["history"][-7:]):
        st.write(f"✅ {item['date']} — {item['topic']}")
else:
    st.info("No history yet. Start today.")

# ---------------- NEXT PREVIEW ----------------
if data["history"]:
    last_topic = data["history"][-1]["topic"]
    st.divider()
    st.markdown("### 🔮 Tomorrow")
    st.write(f"Continue from **{last_topic}** or choose something new.")

# ---------------- EXPORT ----------------
st.divider()
st.markdown("### ⬇️ Backup Your Data")

st.download_button(
    "Download Study History",
    json.dumps(data, indent=2),
    "study_history.json"
)

# ---------------- ABOUT ----------------
with st.expander("ℹ️ About Daily Study OS"):
    st.markdown("""
**Daily Study OS** is built for real students who feel stuck.

It helps you:
- focus on just today
- finish one thing
- feel progress
- come back tomorrow

No syllabus.  
No pressure.  
No limits.  

Built with ❤️ for consistency, not perfection.
""")
