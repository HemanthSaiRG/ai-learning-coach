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
    return {"current_phase": None, "history": []}

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

data = load_data()

# ---------------- HEADER ----------------
st.markdown("## 📘 Daily Study OS")
st.caption("A simple daily guide for students who feel stuck")

# ---------------- PHASE SETUP ----------------
if not data["current_phase"]:
    st.markdown("### 🎯 Set your current learning phase")
    phase = st.text_input("Example: DSA Preparation, Exam Revision, Learning Python")
    if st.button("Start"):
        if phase.strip():
            data["current_phase"] = phase.strip()
            save_data(data)
            st.rerun()
    st.stop()

# ---------------- PHASE BAR ----------------
col1, col2 = st.columns([3,1])
col1.markdown(f"**Current Phase:** {data['current_phase']}")
if col2.button("Change Phase"):
    data["current_phase"] = None
    save_data(data)
    st.rerun()

st.divider()

# ---------------- TODAY STUDY ----------------
st.markdown("### 📌 Today's Focus")
topic = st.text_input("What are you studying today?")

if st.button("Mark as Done"):
    if topic.strip():
        data["history"].append({
            "date": str(date.today()),
            "topic": topic.strip(),
            "status": "done"
        })
        save_data(data)
        st.success("You're done for today 🌱 See you tomorrow")
        st.rerun()

# ---------------- HISTORY ----------------
st.divider()
st.markdown("### 📅 Study History")

if data["history"]:
    for item in reversed(data["history"][-7:]):
        st.write(f"✅ {item['date']} — {item['topic']}")
else:
    st.info("No history yet. Start today.")

# ---------------- NEXT STEP PREVIEW ----------------
if data["history"]:
    last_topic = data["history"][-1]["topic"]
    st.divider()
    st.markdown("### 🔮 Tomorrow")
    st.write(f"Continue from **{last_topic}** or pick a new topic.")

# ---------------- ABOUT ----------------
with st.expander("ℹ️ About this app"):
    st.markdown("""
**Daily Study OS** helps you:
- decide what to study today
- finish it
- feel progress
- come back tomorrow

No syllabus.  
No pressure.  
No limits.  

Built for real students who feel stuck.
""")
