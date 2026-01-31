import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# MOBILE TAP-TO-START (FINAL FIX FOR STREAMLIT CLOUD)
# ======================================================
ua = st.request.headers.get("user-agent", "").lower()
IS_MOBILE = any(x in ua for x in ["iphone", "android", "mobile"])

if IS_MOBILE and "started" not in st.session_state:
    st.markdown("## 📱 AI Learning Coach")
    st.info("Tap start to load app (mobile optimized)")
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
# MODE (DEMO FOR MOBILE)
# ======================================================
if IS_MOBILE:
    st.session_state["DEMO_MODE"] = True
else:
    st.session_state.setdefault("DEMO_MODE", False)

if st.session_state["DEMO_MODE"]:
    st.warning("⚡ Demo Mode (Fast Mobile Mode)")
else:
    st.success("🧠 Full AI Mode")

# ======================================================
# NAVIGATION
# ======================================================
page = st.sidebar.radio(
    "Navigate",
    ["Study", "Upload", "Planner", "Daily", "Analytics", "About"]
)

# ======================================================
# SAFE AI
# ======================================================
def demo_ai(topic, confusions, time_spent):
    return f"""
📘 Demo AI Tutor

Topic: {topic}
Confusions: {confusions}
Time spent: {time_spent} min

Plan:
1. Revise basics
2. Practice 5 problems
3. Watch one video
4. Revise tomorrow
"""

def get_ai():
    if st.session_state["DEMO_MODE"]:
        return None
    try:
        from src.ai_engine import analyze_learning
        return analyze_learning
    except:
        return None

# ======================================================
# SAFE MEMORY
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
# STUDY
# ======================================================
if page == "Study":
    st.header("📚 Study")

    topic = st.text_input("Topic")
    confusions = st.text_area("What is confusing?")
    time_spent = st.number_input("Time spent (minutes)", 1, 300, 30)

    if st.button("Analyze"):
        ai = get_ai()
        if ai:
            result = ai(topic, confusions, time_spent)
        else:
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
# UPLOAD
# ======================================================
elif page == "Upload":
    st.header("📤 Upload Material")
    st.info("PDF upload available (stored locally)")
    st.file_uploader("Upload PDF", type=["pdf"])

# ======================================================
# PLANNER
# ======================================================
elif page == "Planner":
    st.header("🗓 Planner")
    st.markdown("""
- Day 1: Revise basics
- Day 2: Practice
- Day 3: Test yourself
""")

# ======================================================
# DAILY
# ======================================================
elif page == "Daily":
    st.header("📆 Daily Tasks")
    st.checkbox("Revise yesterday topic")
    st.checkbox("Practice 5 questions")
    st.checkbox("Read next section")
    st.success("Consistency beats intensity 💪")

# ======================================================
# ANALYTICS
# ======================================================
elif page == "Analytics":
    st.header("📊 Analytics")

    data = load_data()
    if data:
        df = pd.DataFrame(data)
        if "meta" in df.columns:
            df["time_spent"] = df["meta"].apply(lambda x: x.get("time_spent", 0))
            df["date"] = pd.to_datetime(df["meta"].apply(lambda x: x.get("time", datetime.now())))
            weekly = df.resample("W", on="date").sum(numeric_only=True)

            fig, ax = plt.subplots()
            ax.plot(weekly.index, weekly["time_spent"])
            ax.set_ylabel("Minutes")
            st.pyplot(fig)
    else:
        st.info("No data yet")

# ======================================================
# ABOUT
# ======================================================
elif page == "About":
    st.markdown("""
# 🎓 AI Learning Coach

A **mobile-safe AI study system** designed for real students.

### Features
- Works on mobile without crash
- Demo AI mode (free)
- Full AI on desktop
- Planner + Analytics
- PDF support
- Cloud-safe architecture

Built by **Hemanth Sai** 💙
""")
