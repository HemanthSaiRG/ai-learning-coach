import streamlit as st
from src.export_engine import export_workspace, import_workspace

def export_ui(user_dir):
    st.subheader("📦 Backup / Restore")

    if st.button("Export My Data"):
        export_workspace(user_dir, user_dir)
        st.success("Exported successfully!")

    uploaded = st.file_uploader("Import backup", type=["zip"])
    if uploaded:
        import_workspace(uploaded, user_dir)
        st.success("Imported successfully!")
