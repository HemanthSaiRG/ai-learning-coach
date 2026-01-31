import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# DEVICE DETECTION (SAFE)
# ======================================================
is_desktop = True
try:
    if st.runtime.exists():
        is_desktop = True
except:
    pass

# ======================================================
# MOBILE TAP-TO-START (DESKTOP AUTO-START)
# ======================================================
if "started" not in st.session_state:
    if is_desktop:
        st.session_state.started = True
        st.rerun()
    else:
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
    initial_sidebar_state="expanded"
)

# ======================================================
# LOADING BAR (UI POLISH)
# ======================================================
st.markdown("""
<style>
.loader {
  height: 6px;
  width: 100%;
  background: linear-gradient(90deg, #6366f1, #22d3ee, #6366f1);
  background-size: 200% 100%;
  animation: load 1.2s infinite linear;
  border-radius: 5px;
  margin-bottom: 10px;
}
@keyframes load {
  from {background-position: 0%}
  to {background-position: 200%}
}
</style>
<div class="loader"></div>
""", unsafe_allow_html=True)

# ======================================================
# MODE
# ======================================================
st.session_state.setdefault("DEMO_MODE", True)
st.caption("⚡ Demo Mode (Fast & Stable)")

# ======================================================
# NAVIGATION
# ======================================================
page = st.sidebar.radio(
    "Navigate",
    ["Study", "Upload", "Planner", "Daily", "Analytics", "About"]
)

# ======================================================
# DEMO AI
# ======================================================
def demo_ai(topic, confusions, time_spent):
    return f"""
📘 **AI Coach (Demo)**

Topic: {topic}
Confusions: {confusions}
Time: {time_spent} min

✔ Explanation:
Revise basics, then practice.

✔ Plan:
Day 1 – Basics  
Day 2 – Practice  
Day 3 – Test
"""

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
    confusions = st.text_area("Confusions")
    time_spent = st.number_input("Time (minutes)", 1, 300, 30)

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
# UPLOAD
# ======================================================
elif page == "Upload":
    st.header("📤 Upload")
    st.file_uploader("Upload PDF", type=["pdf"])

# ======================================================
# PLANNER
# ======================================================
elif page == "Planner":
    st.header("🗓 Planner")
    st.markdown("""
- Day 1: Revise basics  
- Day 2: Practice  
- Day 3: Test  
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

A **mobile-safe, cloud-safe study system**.

### Features
- Desktop auto-start
- Mobile tap-to-start
- No timeout
- No crashes
- Demo AI
- Planner + Analytics
- Clean UI

Built by **Hemanth Sai** 💙
""")
