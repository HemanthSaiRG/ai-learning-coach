import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# TAP TO START (FINAL MOBILE + CLOUD SAFE FIX)
# ======================================================
if "started" not in st.session_state:
    st.markdown("## 🚀 AI Learning Coach")
    st.info("Tap start to load app (prevents mobile timeout)")
    if st.button("▶ Start"):
        st.session_state.started = True
        st.rerun()
    st.stop()

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="AI Learning Coach",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ======================================================
# DEMO MODE (SAFE DEFAULT FOR MOBILE)
# ======================================================
st.session_state.setdefault("DEMO_MODE", True)
st.warning("⚡ Demo Mode (Fast & Stable)")

# ======================================================
# NAVIGATION
# ======================================================
page = st.sidebar.radio(
    "Navigate",
    ["Study", "Upload", "Planner", "Daily", "Analytics", "About"]
)

# ======================================================
# DEMO AI (NO DEPENDENCIES)
# ======================================================
def demo_ai(topic, confusions, time_spent):
    return f"""
📘 **Demo AI Tutor**

Topic: {topic}
Confusions: {confusions}
Time spent: {time_spent} min

✅ Explanation:
Revise basics first, then practice 5 problems.

📌 Weak areas:
- Needs revision
- Practice required

📅 Plan:
Day 1: Basics  
Day 2: Practice  
Day 3: Revise & test
"""

# ======================================================
# SAFE MEMORY (NO CRASH)
# ======================================================
def load_data():
    try:
        from src.memory_engine import load_memory
        return load_memory()
    except:
        return []

def save_data(text, meta):
    try:
        from src.memory_engine import add_memory
        add_memory(text, meta)
    except:
        pass

# ======================================================
# STUDY PAGE
# ======================================================
if page == "Study":
    st.header("📚 Study")

    topic = st.text_input("Topic")
    confusions = st.text_area("What is confusing?")
    time_spent = st.number_input("Time spent (minutes)", 1, 300, 30)

    if st.button("Analyze"):
        result = demo_ai(topic, confusions, time_spent)

        save_data(
            f"{topic}: {confusions}",
            {
                "topic": topic,
                "time_spent": time_spent,
                "time": str(datetime.now())
            }
        )

        st.success(result)

# ======================================================
# UPLOAD PAGE
# ======================================================
elif page == "Upload":
    st.header("📤 Upload Material")
    st.file_uploader("Upload PDF", type=["pdf"])

# ======================================================
# PLANNER PAGE
# ======================================================
elif page == "Planner":
    st.header("🗓 Study Planner")
    st.markdown("""
- Day 1: Revise basics  
- Day 2: Practice  
- Day 3: Mock test  
""")

# ======================================================
# DAILY PAGE
# ======================================================
elif page == "Daily":
    st.header("📆 Daily Tasks")
    st.checkbox("Revise yesterday topic")
    st.checkbox("Practice 5 questions")
    st.checkbox("Read next section")
    st.success("Consistency beats intensity 💪")

# ======================================================
# ANALYTICS PAGE
# ======================================================
elif page == "Analytics":
    st.header("📊 Analytics")

    data = load_data()
    if data:
        df = pd.DataFrame(data)
        if "meta" in df.columns:
            df["time_spent"] = df["meta"].apply(lambda x: x.get("time_spent", 0))
            df["date"] = pd.to_datetime(
                df["meta"].apply(lambda x: x.get("time", datetime.now()))
            )

            weekly = df.resample("W", on="date").sum(numeric_only=True)

            fig, ax = plt.subplots()
            ax.plot(weekly.index, weekly["time_spent"])
            ax.set_title("Weekly Study Time")
            ax.set_ylabel("Minutes")
            st.pyplot(fig)
    else:
        st.info("No data yet")

# ======================================================
# ABOUT PAGE
# ======================================================
elif page == "About":
    st.markdown("""
# 🎓 AI Learning Coach

A **mobile-safe AI study system** built for students.

### Features
- No mobile timeout
- Works on slow internet
- Demo AI mode (free)
- Planner + Analytics
- PDF upload
- Cloud safe

Built by **Hemanth Sai** 💙
""")
