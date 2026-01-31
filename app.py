import streamlit as st
from datetime import datetime

from ui.components import header, input_form
from ui.auth_ui import login_ui
from ui.upload_ui import upload_ui
from src.ai_engine import analyze_learning
from src.memory_engine import add_memory, load_memory

# -------------------------------------------------
# PAGE CONFIG (MOBILE SAFE)
# -------------------------------------------------
st.set_page_config(
    page_title="AI Learning Coach",
    layout="centered",
    initial_sidebar_state="collapsed"  # 👈 mobile fix
)

# -------------------------------------------------
# MOBILE LOADER (INSTANT FEEDBACK)
# -------------------------------------------------
st.markdown(
    """
    <style>
    .mobile-loader {
        height: 6px;
        background: linear-gradient(90deg, #4f46e5, #22d3ee, #4f46e5);
        background-size: 200% 100%;
        animation: move 1.2s linear infinite;
        border-radius: 10px;
        margin-bottom: 12px;
    }
    @keyframes move {
        0% {background-position: 0%}
        100% {background-position: 200%}
    }
    </style>
    <div class="mobile-loader"></div>
    """,
    unsafe_allow_html=True
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
# ANALYTICS PAGE (LOAD ON DEMAND - MOBILE SAFE)
# -------------------------------------------------
elif page == "Analytics":
    st.subheader("📈 Weekly Analytics")
    st.caption("Tap button to load (optimized for mobile)")

    if st.button("Load analytics"):
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
# DAILY PAGE (OFFLINE DEMO AI)
# -------------------------------------------------
elif page == "Daily":
    st.subheader("🧠 Daily Coach (Demo Mode)")

    st.markdown("""
    ### 🎯 Today’s Smart Plan
    - Revise yesterday's topic
    - Practice 5 questions
    - Read next section
    - 45–60 min deep focus
    - Note confusions

    💡 Tip: Consistency beats intensity.
    """)

    st.success("✅ Generated in demo mode (no AI credits used)")

# -------------------------------------------------
# ABOUT PAGE (PREMIUM FEEL)
# -------------------------------------------------
elif page == "About":
    st.markdown("""
    ## 🎓 AI Learning Coach

    A **mobile-first, offline-first intelligent study system** built to help
    students learn smarter — not harder.

    ### ✨ What makes it special
    - Personal workspace
    - Smart memory
    - Weekly analytics
    - PDF upload
    - Demo AI mode
    - Cloud safe
    - Mobile optimized

    ### 🛠 Built with
    - Streamlit
    - Python
    - Clean architecture
    - Production mindset

    ---
    **Built with ❤️ by Hemanth**
    """)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption("AI Learning Coach v1.1 • Mobile Optimized Release")
