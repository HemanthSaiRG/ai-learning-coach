import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

from ui.components import header, input_form
from ui.auth_ui import login_ui
from ui.upload_ui import upload_ui
from src.ai_engine import analyze_learning
from src.memory_engine import add_memory, load_memory

st.set_page_config(page_title="AI Learning Coach", layout="centered")

# ---------- AUTH ----------
if "user" not in st.session_state:
    login_ui()
    st.stop()

# ---------- USER WORKSPACE ----------
user_dir = f"data/users/{st.session_state['user']}"
os.makedirs(user_dir, exist_ok=True)

# ---------- PDF UPLOAD ----------
upload_ui(user_dir)

# ---------- UI ----------
header()

topic, confusions, time_spent, submitted = input_form()

if submitted:
    # ✅ UPDATED AI CALL (user-specific)
    result = analyze_learning(topic, confusions, time_spent, user_dir)

    # ---------- SAVE MEMORY ----------
    add_memory(
        f"{topic}. Confusions: {confusions}",
        {
            "topic": topic,
            "time_spent": time_spent,
            "user": st.session_state["user"]
        }
    )

    # ---------- AUTO PROGRESS TRACKING ----------
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

    st.subheader("Analysis Result")
    st.success(result)

# ---------- DASHBOARD ----------
st.divider()
st.subheader("📈 Weekly Analytics")

data = load_memory()

# ✅ filter data per user
data = [d for d in data if d.get("meta", {}).get("user") == st.session_state["user"]]

if data:
    df = pd.DataFrame(data)

    if "time" in df.columns:
        df["date"] = pd.to_datetime(df["time"], errors="coerce")
    else:
        df["date"] = datetime.now()

    df["time_spent"] = df["meta"].apply(
        lambda x: x.get("time_spent", 0) if isinstance(x, dict) else 0
    )

    weekly = df.resample("W", on="date").sum(numeric_only=True)

    fig, ax = plt.subplots()
    ax.plot(weekly.index, weekly["time_spent"])
    ax.set_title("Weekly Study Time")
    ax.set_ylabel("Minutes")
    st.pyplot(fig)

    # ---------- INSIGHTS ----------
    st.subheader("🧩 Insights")
    most_common = (
        df["meta"]
        .apply(lambda x: x.get("topic") if isinstance(x, dict) else None)
        .value_counts()
        .head(3)
    )

    if not most_common.empty:
        st.write("Most studied topics:")
        st.write(most_common)
    else:
        st.info("No topics yet.")

else:
    st.info("No data yet. Start studying to see analytics.")
