import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from ui.components import header, input_form
from src.ai_engine import analyze_learning
from src.memory_engine import add_memory, load_memory

st.set_page_config(page_title="AI Learning Coach", layout="centered")

# ---------- UI ----------
header()

topic, confusions, time_spent, submitted = input_form()

if submitted:
    result = analyze_learning(topic, confusions, time_spent)

    add_memory(
        f"{topic}. Confusions: {confusions}",
        {
            "topic": topic,
            "time_spent": time_spent
        }
    )

    st.subheader("Analysis Result")
    st.success(result)

# ---------- DASHBOARD ----------
st.divider()
st.subheader("📈 Weekly Analytics")

data = load_memory()

if data:
    df = pd.DataFrame(data)

    # ✅ SAFE date handling (no KeyError)
    if "time" in df.columns:
        df["date"] = pd.to_datetime(df["time"], errors="coerce")
    else:
        df["date"] = datetime.now()

    # ✅ SAFE meta handling
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
