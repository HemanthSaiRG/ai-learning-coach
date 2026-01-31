import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

from ui.components import header, input_form
from ui.auth_ui import login_ui
from ui.upload_ui import upload_ui
from ui.planner_ui import planner_ui
from ui.export_ui import export_ui
from src.ai_engine import analyze_learning
from src.memory_engine import add_memory, load_memory

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Study OS",
    page_icon="🎓",
    layout="wide"
)

# ---------- AUTH ----------
if "user" not in st.session_state:
    login_ui()
    st.stop()

# ---------- USER WORKSPACE ----------
user_dir = f"data/users/{st.session_state['user']}"
os.makedirs(user_dir, exist_ok=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown(f"### 👤 {st.session_state['user']}")
page = st.sidebar.radio(
    "Navigate",
    [
        "📘 Study",
        "📄 Upload",
        "🗓 Planner",
        "☀️ Daily",
        "📊 Analytics",
        "💾 Backup",
        "ℹ️ About"
    ]
)

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
h1, h2, h3 { color: #2E86C1; }
.block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 📘 STUDY PAGE
# ==========================================================
if page == "📘 Study":
    header()
    st.markdown("### 🧠 Learn smarter, not harder")

    topic, confusions, time_spent, submitted = input_form()

    if submitted:
        result = analyze_learning(topic, confusions, time_spent, user_dir)

        # Save memory
        add_memory(
            f"{topic}. Confusions: {confusions}",
            {
                "topic": topic,
                "time_spent": time_spent,
                "user": st.session_state["user"]
            }
        )

        # Progress tracking
        progress_file = f"{user_dir}/subjects.json"
        try:
            with open(progress_file, "r") as f:
                subjects = json.load(f)
        except:
            subjects = []

        subjects.append({
            "topic": topic,
            "time_spent": time_spent,
            "status": "studied",
            "date": datetime.now().isoformat()
        })

        with open(progress_file, "w") as f:
            json.dump(subjects, f, indent=2)

        st.subheader("✅ AI Feedback")
        st.success(result)

# ==========================================================
# 📄 UPLOAD PAGE
# ==========================================================
if page == "📄 Upload":
    st.markdown("## 📄 Upload Study Material")
    upload_ui(user_dir)

# ==========================================================
# 🗓 PLANNER PAGE
# ==========================================================
if page == "🗓 Planner":
    st.markdown("## 🗓 Study Planner")
    planner_ui(user_dir)

# ==========================================================
# ☀️ DAILY PAGE (NEW INTELLIGENCE)
# ==========================================================
if page == "☀️ Daily":
    st.markdown("## ☀️ Daily Focus")

    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = f"{user_dir}/daily.json"

    if os.path.exists(daily_file):
        with open(daily_file, "r") as f:
            daily = json.load(f)
    else:
        daily = {}

    focus = st.text_input("🎯 What will you focus on today?", daily.get(today, ""))

    if st.button("Save Today’s Focus"):
        daily[today] = focus
        with open(daily_file, "w") as f:
            json.dump(daily, f, indent=2)
        st.success("Saved! Stay consistent 💪")

    if daily.get(today):
        st.info(f"📌 Today’s focus: **{daily[today]}**")

# ==========================================================
# 📊 ANALYTICS PAGE
# ==========================================================
if page == "📊 Analytics":
    st.markdown("## 📊 Learning Analytics")

    data = load_memory()
    data = [d for d in data if d.get("meta", {}).get("user") == st.session_state["user"]]

    if data:
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df.get("time", datetime.now()), errors="coerce")
        df["time_spent"] = df["meta"].apply(
            lambda x: x.get("time_spent", 0) if isinstance(x, dict) else 0
        )

        weekly = df.resample("W", on="date").sum(numeric_only=True)

        fig, ax = plt.subplots()
        ax.plot(weekly.index, weekly["time_spent"])
        ax.set_title("Weekly Study Time")
        ax.set_ylabel("Minutes")
        st.pyplot(fig)

        st.markdown("### 🔁 Most Studied Topics")
        st.write(
            df["meta"]
            .apply(lambda x: x.get("topic") if isinstance(x, dict) else None)
            .value_counts()
            .head(5)
        )
    else:
        st.info("No data yet.")

# ==========================================================
# 💾 BACKUP PAGE
# ==========================================================
if page == "💾 Backup":
    st.markdown("## 💾 Export & Backup")
    export_ui(user_dir)

# ==========================================================
# ℹ️ ABOUT PAGE (PREMIUM)
# ==========================================================
if page == "ℹ️ About":
    st.markdown("""
    ## 🎓 AI Study OS

    **AI Study OS** is an offline-first intelligent learning system that helps students
    study smarter using AI, memory, and analytics.

    ### 🚀 Features
    - AI Tutor (PDF + RAG based)
    - Automatic progress tracking
    - Study planner & daily focus
    - Learning analytics
    - Multi-user workspace
    - Offline-first design
    - Cloud deployable

    ### 🧠 Built With
    - Streamlit
    - Python
    - JSON-based memory
    - RAG architecture
    - Modular UI design

    ### 👨‍💻 Author
    **Hemanth Sai**  
    B.Tech CSE | Final Year Project  
    Built with ❤️ and real engineering thinking.

    ---
    _“Don’t just study harder. Study smarter.”_
    """)
