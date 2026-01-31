import streamlit as st
from datetime import date
from src.reminder_engine import save_reminder, load_reminders
from src.readiness_engine import calculate_readiness

def daily_ui(user_dir):
    st.subheader("📅 Daily Study & Reminders")

    reminder = st.text_input("Add reminder for today")
    if st.button("Add Reminder"):
        save_reminder(user_dir, reminder, str(date.today()))
        st.success("Reminder added!")

    reminders = load_reminders(user_dir)
    for r in reminders:
        if r["date"] == str(date.today()):
            st.checkbox(r["text"], value=r["done"])

    st.divider()
    st.subheader("🎯 Exam Readiness")

    score = calculate_readiness(user_dir)
    st.progress(score)
    st.write(f"Readiness Score: {score}%")
