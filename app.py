import streamlit as st

# =================================================
# FORCE FIRST PAINT (MOBILE FIX)
# =================================================
if "booted" not in st.session_state:
    st.session_state.booted = True
    st.markdown("## 🚀 AI Learning Coach is starting…")
    st.markdown("⏳ Please wait 2–3 seconds")
    st.stop()

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="AI Learning Coach",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =================================================
# MOBILE DETECTION (SIMPLE + SAFE)
# =================================================
is_mobile = st.session_state.get("is_mobile", False)
ua = st.request.headers.get("user-agent", "").lower()
if any(x in ua for x in ["iphone", "android", "mobile"]):
    is_mobile = True
st.session_state.is_mobile = is_mobile

# =================================================
# CSS FOR BOTTOM NAV (MOBILE ONLY)
# =================================================
if is_mobile:
    st.markdown("""
    <style>
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #0f172a;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 9999;
        border-top: 1px solid #1e293b;
    }
    .bottom-nav button {
        background: none;
        border: none;
        color: #cbd5f5;
        font-size: 12px;
    }
    .bottom-nav button.active {
        color: #22d3ee;
        font-weight: bold;
    }
    .spacer {
        height: 70px;
    }
    </style>
    """, unsafe_allow_html=True)

# =================================================
# NAVIGATION STATE
# =================================================
if "page" not in st.session_state:
    st.session_state.page = "Study"

# =================================================
# DESKTOP NAV (SIDEBAR)
# =================================================
if not is_mobile:
    st.session_state.page = st.sidebar.radio(
        "Navigate",
        ["Study", "Upload", "Analytics", "Daily", "About"]
    )

# =================================================
# AUTH
# =================================================
from ui.auth_ui import login_ui

if "user" not in st.session_state:
    login_ui()
    st.stop()

user = st.session_state["user"]
user_dir = f"data/users/{user}"

# =================================================
# IMPORTS (AFTER BOOT)
# =================================================
from datetime import datetime
from ui.components import header, input_form
from ui.upload_ui import upload_ui
from src.ai_engine import analyze_learning
from src.memory_engine import add_memory, load_memory

# =================================================
# PAGE ROUTER
# =================================================
page = st.session_state.page

# ---------------- STUDY ----------------
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

# ---------------- UPLOAD ----------------
elif page == "Upload":
    st.subheader("📄 Upload Study Material")
    upload_ui(user_dir)

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.subheader("📈 Weekly Analytics")
    if st.button("Load analytics"):
        import pandas as pd
        import matplotlib.pyplot as plt

        data = load_memory()
        data = [d for d in data if d.get("meta", {}).get("user") == user]

        if data:
            df = pd.DataFrame(data)
            df["date"] = pd.to_datetime(df["time"], errors="coerce")
            df["time_spent"] = df["meta"].apply(
                lambda x: x.get("time_spent", 0) if isinstance(x, dict) else 0
            )

            weekly = df.resample("W", on="date").sum(numeric_only=True)

            fig, ax = plt.subplots()
            ax.plot(weekly.index, weekly["time_spent"])
            ax.set_ylabel("Minutes")
            st.pyplot(fig)

# ---------------- DAILY ----------------
elif page == "Daily":
    st.subheader("🧠 Daily Coach")
    st.markdown("""
    - Revise last topic  
    - Practice 5 questions  
    - Read next section  
    - 45–60 min focus  
    """)
    st.success("Demo plan generated")

# ---------------- ABOUT ----------------
elif page == "About":
    st.markdown("""
    ## 🎓 AI Learning Coach

    A **mobile-first intelligent study OS**.

    Built with ❤️ by Hemanth  
    Version: **v1.3**
    """)

# =================================================
# MOBILE BOTTOM NAV
# =================================================
if is_mobile:
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    cols = st.columns(5)

    buttons = ["Study", "Upload", "Analytics", "Daily", "About"]
    icons = ["📘", "📄", "📊", "🧠", "ℹ️"]

    with st.container():
        st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
        for b, icon in zip(buttons, icons):
            active = "active" if page == b else ""
            if st.button(f"{icon}\n{b}", key=f"nav-{b}"):
                st.session_state.page = b
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
