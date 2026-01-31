import streamlit as st
from datetime import datetime

from ui.components import header, input_form
from ui.auth_ui import login_ui
from ui.upload_ui import upload_ui
from src.ai_engine import analyze_learning
from src.memory_engine import add_memory, load_memory

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Learning Coach",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.info("🚀 Starting AI Learning Coach...")

# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------
page = st.sidebar.radio(
    "Navigate",
    ["Study", "Upload", "Analytics", "Daily", "About"]
)

# -------------------------------------------------
# AUTH
# -------------------------------------------------
if "user" not in st.session_state:
    login_ui()
    st.stop()

user = st.session_state["user"]
user_dir = f"data/users/{user}"

# -------------------------------------------------
# STUDY PAGE
# -------------------------------------------------
if page == "Study":
    header()

    topic, confusions, time_spent, submitted = input_form()

    if submitted:
        with st.spinner("Analyzing..."):
            result = analyze_learning(topic, confusions, time_spent)

        add_memory(
            f"{topic}. Confusions: {confusions}",
            {
                "topic": topic,
                "time_spent": time_spent,
                "user": user
            }
        )

        st.subheader("📊 Analysis Result")
        st.success(result)

# -------------------------------------------------
# UPLOAD PAGE
# -------------------------------------------------
elif page == "Upload":
    st.subheader("📄 Upload Study Material")
    upload_ui(user_dir)

# -------------------------------------------------
# ANALYTICS PAGE (LAZY IMPORTS = NO FREEZE)
# -------------------------------------------------
elif page == "Analytics":
    st.subheader("📈 Weekly Analytics")

    with st.spinner("Loading analytics..."):
        import pandas as pd
        import matplotlib.pyplot as plt

        data = load_memory()
        data = [d for d in data if d.get("meta", {}).get("user") == user]

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
            st.info("No data yet. Start studying!")

# -------------------------------------------------
# DAILY PAGE (DEMO LOGIC)
# -------------------------------------------------
elif page == "Daily":
    st.subheader("🧪 Daily Coach (Demo Mode)")

    st.markdown("""
    **Today’s Focus**
    - Revise last topic
    - Practice 5 questions
    - Read next section
    - 45–60 min deep focus
    """)

    st.success("✅ Demo plan generated (offline mode)")

# -------------------------------------------------
# ABOUT PAGE (PREMIUM FEEL)
# -------------------------------------------------
elif page == "About":
    st.markdown("""
    ## 🎓 AI Study OS

    An **offline-first intelligent learning system** that helps students:

    - Study smarter
    - Track progress
    - Upload material
    - Get AI guidance
    - Analyze performance

    ### ✨ Features
    - Personal workspace
    - Smart memory
    - Weekly analytics
    - Upload PDFs
    - Demo AI (no billing needed)
    - Cloud safe
    - Production ready

    ### 🚀 Built With
    - Streamlit
    - Python
    - AI logic
    - Clean architecture

    ---
    **Built with ❤️ by Hemanth**
    """)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption("AI Learning Coach v1.0 • Stable Release")
