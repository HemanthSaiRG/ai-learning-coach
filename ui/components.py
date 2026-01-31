import streamlit as st

def header():
    st.title("AI Learning Coach")
    st.caption("Track your study. Improve daily.")

def input_form():
    with st.form("study_form"):
        topic = st.text_input("What did you study?")
        confusions = st.text_area("What confused you?")
        time_spent = st.number_input("Time spent (minutes)", min_value=0)
        submitted = st.form_submit_button("Analyze")

    return topic, confusions, time_spent, submitted
