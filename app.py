import streamlit as st
from datetime import datetime
import pandas as pd

# ======================================================
# TAP TO START (CLOUD + MOBILE SAFE)
# ======================================================
if "started" not in st.session_state:
    st.markdown("## 🚀 AI Learning Coach")
    st.caption("Optimized for cloud & mobile")
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
# VERSION BANNER
# ======================================================
st.caption("v1.4 • Stable • Demo Mode")

# ======================================================
# DEMO MODE (SAFE DEFAULT)
# ======================================================
st.session_state.setdefault("DEMO_MODE", True)

st.info("⚡ Running in Demo Mode (fast & stable)")

# ======================================================
# NAVIGATION
# ======================================================
page = st.sidebar.radio(
    "Navigate",
    ["Study", "Planner", "Daily", "Analytics", "About"]
)

# ======================================================
# DEMO AI
# ======================================================
def demo_ai(topic, confusions, time_spent):
    return f"""
### 📘 AI Coach (Demo)

**Topic:** {topic}  
**Confusions:** {confusions}  
**Time:** {time_spent} minutes

#### ✅ Explanation
Revise basics → practice → revise again

#### 📅 3-Day Plan
- Day 1: Basics
- Day 2: Practice
- Day 3: Test yourself
"""

# ======================================================
# MEMORY (CACHED)
# ======================================================
@st.cache_data
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
    st.header("📚 Study Session")

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
# PLANNER
# ======================================================
elif page == "Planner":
    st.header("🗓 Study Planner")
    st.markdown("""
- **Day 1**: Revise basics  
- **Day 2**: Practice problems  
- **Day 3**: Self-test  
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
# ANALYTICS (DESKTOP ONLY)
# ======================================================
elif page == "Analytics":
    st.header("📊 Analytics")

    if st.session_state.get("is_mobile", False):
        st.info("📱 Analytics are best viewed on desktop")
    else:
        data = load_data()
        if data:
            df = pd.DataFrame(data)
            if "meta" in df.columns:
                df["time_spent"] = df["meta"].apply(lambda x: x.get("time_spent", 0))
                df["date"] = pd.to_datetime(
                    df["meta"].apply(lambda x: x.get("time", datetime.now()))
                )

                weekly = df.resample("W", on="date").sum(numeric_only=True)
                st.bar_chart(weekly["time_spent"])
        else:
            st.info("No data yet")

# ======================================================
# ABOUT
# ======================================================
elif page == "About":
    st.markdown("""
# 🎓 AI Learning Coach

A **cloud-optimized, mobile-safe study system** designed for students.

### Why this works
- No heavy libraries
- No mobile crashes
- Demo mode for stability
- Cached data
- Native charts
- Clean UI
- Production-ready

### Tech
- Streamlit
- Python
- Clean architecture

**Built by Hemanth** 💙
""")
