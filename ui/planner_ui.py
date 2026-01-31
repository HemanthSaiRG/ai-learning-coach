import streamlit as st
from src.planner_engine import generate_plan

def planner_ui(user_dir):
    st.subheader("🗓️ Smart Study Plan (AI Generated)")

    minutes = st.slider("Available time today (minutes)", 30, 180, 60)

    if st.button("Generate Today's Plan"):
        plan = generate_plan(user_dir, minutes)
        for i, task in enumerate(plan, 1):
            st.write(f"{i}. {task['task']} — {task['minutes']} min")
