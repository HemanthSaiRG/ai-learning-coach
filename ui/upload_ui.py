import streamlit as st
from src.pdf_engine import build_kb

def upload_ui(user_dir):
    st.subheader("📚 Upload Study Material")

    pdf = st.file_uploader("Upload PDF (textbook, notes, syllabus)", type=["pdf"])

    if pdf and st.button("Build Knowledge Base"):
        with st.spinner("Processing PDF..."):
            build_kb(pdf, user_dir)
        st.success("Knowledge base created! AI can now study from this.")
