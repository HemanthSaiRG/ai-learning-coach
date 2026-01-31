import streamlit as st
from src.workspace_manager import init_user

def login_ui():
    st.title("🔐 Login / Signup")

    username = st.text_input("Enter username (no spaces)")
    if st.button("Continue"):
        if username.strip() == "":
            st.error("Username required")
            return None
        st.session_state["user"] = username
        init_user(username)
        st.success(f"Workspace ready for {username}")
        st.rerun()
