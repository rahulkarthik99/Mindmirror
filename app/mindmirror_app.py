import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Engines
from engines import (
    thought_analyzer,
    distortion_detector,
    emotion_engine,
    personality_mapper,
    clarity_engine
)

from app import (
    reflection_journal,
    daily_checkin,
    insight_share_engine,
    therapist_chat,
    health_check
)

__version__ = "1.0.0"

st.set_page_config(
    page_title="MindMirror",
    page_icon="🧠",
    layout="wide"
)

# ------------------------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------------------------

if "journal" not in st.session_state:
    st.session_state.journal = []

if "daily_checkins" not in st.session_state:
    st.session_state.daily_checkins = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_user_msg" not in st.session_state:
    st.session_state.last_user_msg = None

if "show_health" not in st.session_state:
    st.session_state.show_health = False


# ------------------------------------------------
# BASIC CSS
# ------------------------------------------------

st.markdown("""
<style>

.big-title{
font-size:3rem;
font-weight:800;
text-align:center;
margin-bottom:10px;
}

.subtitle{
text-align:center;
color:gray;
margin-bottom:30px;
}

.card{
background:#f8fafc;
padding:20px;
border-radius:12px;
border:1px solid #e2e8f0;
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

with st.sidebar:

    st.markdown(f"### 🧠 MindMirror v{__version__}")

    if st.session_state.daily_checkins:
        streak = daily_checkin.get_streak(st.session_state)
        st.markdown(f"🔥 **Current streak:** {streak} days")

    if st.session_state.journal:
        st.markdown(f"📝 **Total reflections:** {len(st.session_state.journal)}")

    st.divider()

    st.markdown("### ✨ Premium Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("🎤 Voice input")
        st.markdown("📊 Deep analytics")

    with col2:
        st.markdown("🧘 Exercises")
        st.markdown("📈 Patterns")

    st.caption("Coming soon")

    st.divider()

    st.session_state.show_health = st.checkbox("Show System Health")

# ------------------------------------------------
# SYSTEM HEALTH
# ------------------------------------------------

if st.session_state.show_health:

    with st.expander("🔧 System Health"):

        health = health_check()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("App Version", health["app"]["version"])

        with col2:
            st.metric("API Status", health["configuration"]["status"])

        with col3:
            st.metric("Overall", health["overall"])

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown("<div class='big-title'>🧠 MindMirror</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Understand your thoughts. Gain clarity.</div>", unsafe_allow_html=True)

# ------------------------------------------------
# TABS
# ------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
"🔍 Reflection",
"📓 Journal",
"📊 Daily Check-In",
"💬 AI Therapist"
])

# =================================================
# TAB 1 REFLECTION
# =================================================

with tab1:

    st.markdown("### What's on your mind?")

    user_input = st.text_area(
        "",
        height=150,
        placeholder="Write freely. This is your private reflection space."
    )

    if st.button("🔍 Analyze Thought", type="primary", use_container_width=True):

        if user_input.strip() == "":
            st.warning("Please write something first.")
            st.stop()

        with st.spinner("Analyzing your thought..."):

            analysis = thought_analyzer.analyze_thought(user_input)

            distortions = distortion_detector.detect_distortions(user_input)

            emotions = emotion_engine.generate_emotion_profile(user_input)

            personality = personality_mapper.build_personality_profile(user_input)

            clarity = clarity_engine.build_clarity_report(
                emotions,
                distortions,
                personality
            )

            reflection_journal.save_reflection(
                st.session_state,
                user_input,
                analysis,
                personality,
                emotions
            )

        st.markdown("## 📝 Reflection")

        st.markdown(
            f"<div class='card'>{analysis}</div>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=clarity["score"],
                title={'text': "Clarity Score"},
                gauge={
                    'axis': {'range': [0,100]}
                }
            ))

            st.plotly_chart(fig, use_container_width=True)

        with col2:

            if emotions:

                labels = list(emotions.keys())
                values = list(emotions.values())

                radar = go.Figure()

                radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=labels,
                    fill='toself'
                ))

                st.plotly_chart(radar, use_container_width=True)

        st.markdown("### Cognitive Distortions")

        if distortions:

            for d in distortions:
                st.write("•", d)

        else:
            st.success("No major distortions detected.")

        st.markdown("### MindMirror Archetype")
        st.info(personality["archetype"])

# =================================================
# TAB 2 JOURNAL
# =================================================

with tab2:

    st.markdown("## 📓 Reflection Journal")

    journal = reflection_journal.get_journal(st.session_state)

    if not journal:

        st.info("You haven't created reflections yet.")

    else:

        for entry in reversed(journal):

            with st.expander(entry["date"]):

                st.markdown("**Thought**")
                st.write(entry["thought"])

                st.markdown("**Insight**")
                st.write(entry["analysis"])

# =================================================
# TAB 3 DAILY CHECK
# =================================================

with tab3:

    st.markdown("## 📊 Daily Mind Check")

    mood = st.selectbox(
        "How are you feeling today?",
        [
            "Calm",
            "Motivated",
            "Confused",
            "Anxious",
            "Overwhelmed",
            "Sad"
        ]
    )

    if st.button("Record Mood", use_container_width=True):

        daily_checkin.record_checkin(st.session_state, mood)

        st.success("Mood recorded!")

    streak = daily_checkin.get_streak(st.session_state)

    if streak > 0:
        st.metric("Current streak", f"{streak} days")

# =================================================
# TAB 4 AI THERAPIST
# =================================================

with tab4:

    st.markdown("## 💬 AI Therapist")

    for msg in st.session_state.chat_history:

        if msg["role"] == "system":
            continue

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ------------------------------------------------
# CHAT INPUT
# ------------------------------------------------

user_msg = st.chat_input("Share what's on your mind")

if user_msg and user_msg != st.session_state.last_user_msg:

    st.session_state.last_user_msg = user_msg

    therapist_chat.add_user_message(
        st.session_state,
        user_msg
    )

    with st.spinner("Thinking..."):

        reply = therapist_chat.generate_response(st.session_state)

    therapist_chat.add_assistant_message(
        st.session_state,
        reply
    )

    st.rerun()

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown("---")

st.caption(
"MindMirror • A reflection tool for clarity. Not a substitute for professional mental health care."
)