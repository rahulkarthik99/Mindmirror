import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Engines
from thought_analyzer import analyze_thought
from distortion_detector import detect_distortions
from emotion_engine import generate_emotion_profile
from personality_mapper import build_personality_profile
from clarity_engine import build_clarity_report
from reflection_journal import (
    initialize_journal,
    save_reflection,
    get_journal
)
from daily_checkin import (
    initialize_checkins,
    record_checkin,
    get_checkins,
    get_streak
)
from insight_share_engine import build_share_block
from therapist_chat import (
    initialize_chat,
    add_user_message,
    add_assistant_message,
    generate_response
)

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="MindMirror",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"  # Better for mobile
)

# ------------------------------------------------
# MOBILE-RESPONSIVE CSS (COMPLETE)
# ------------------------------------------------

st.markdown("""
<style>
/* ========================================
   MindMirror Premium - Mobile Responsive CSS
   ======================================== */

/* ---------- Base Reset & Variables ---------- */
:root {
    /* Primary colors */
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --primary-light: #3b82f6;
    --primary-soft: #dbeafe;
    
    /* Semantic colors */
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #6366f1;
    
    /* Neutral colors */
    --background: #ffffff;
    --surface: #f8fafc;
    --surface-hover: #f1f5f9;
    --border: #e2e8f0;
    
    /* Text colors */
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-tertiary: #64748b;
    
    /* Spacing */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;
    
    /* Border radius */
    --radius-sm: 0.375rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    --radius-full: 9999px;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    :root {
        --background: #0f172a;
        --surface: #1e293b;
        --surface-hover: #334155;
        --border: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-tertiary: #94a3b8;
        --primary-soft: #1e3a8a;
    }
}

/* ---------- Base Layout ---------- */
.stApp {
    background: var(--background);
}

.main > div {
    padding: 0 var(--space-md);
}

.block-container {
    max-width: 1200px !important;
    padding: var(--space-lg) var(--space-md) !important;
    margin: 0 auto !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---------- Your Original Styles (Enhanced) ---------- */
.big-title {
    font-size: clamp(2.5rem, 8vw, 3.25rem) !important;
    font-weight: 800;
    text-align: center;
    letter-spacing: -1px;
    margin-bottom: 6px;
    color: var(--text-primary);
    line-height: 1.2;
}

.subtitle {
    text-align: center;
    color: var(--text-secondary);
    margin-bottom: 40px;
    font-size: clamp(1rem, 3vw, 1.125rem);
}

.card {
    background: var(--surface);
    padding: clamp(1rem, 4vw, 1.75rem);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    margin-bottom: 25px;
    border: 1px solid var(--border);
    color: var(--text-secondary);
    line-height: 1.6;
    font-size: clamp(0.95rem, 2vw, 1rem);
}

.section {
    margin-top: 20px;
}

/* ---------- Typography ---------- */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary);
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: var(--space-md);
}

h1 { font-size: clamp(2rem, 5vw, 2.5rem); }
h2 { font-size: clamp(1.5rem, 4vw, 2rem); }
h3 { font-size: clamp(1.25rem, 3vw, 1.5rem); }
h4 { font-size: clamp(1.1rem, 2.5vw, 1.25rem); }

p, li, .stMarkdown {
    color: var(--text-secondary);
    font-size: clamp(1rem, 2vw, 1.05rem);
    line-height: 1.6;
}

/* ---------- Buttons ---------- */
.stButton > button {
    width: 100%;
    background: var(--primary);
    color: white;
    border: none;
    padding: var(--space-md) var(--space-lg);
    border-radius: var(--radius-md);
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    min-height: 48px;  /* Better touch target */
    box-shadow: var(--shadow-sm);
}

.stButton > button:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Primary button variant (your "Analyze Thought" button) */
.stButton > button[kind="primary"] {
    background: var(--primary);
    color: white;
}

/* ---------- Text Areas ---------- */
.stTextArea > div > div > textarea {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    font-size: 1rem;
    width: 100%;
    min-height: 150px;
    color: var(--text-primary);
    transition: all 0.2s ease;
}

.stTextArea > div > div > textarea:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px var(--primary-soft);
    outline: none;
}

/* ---------- Select Boxes ---------- */
.stSelectbox > div > div > div {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    min-height: 48px;
}

/* ---------- Metrics & Stats ---------- */
.stMetric {
    background: var(--surface);
    padding: var(--space-md);
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
}

.stMetric label {
    color: var(--text-tertiary) !important;
    font-size: 0.875rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stMetric .metric-value {
    color: var(--primary) !important;
    font-size: clamp(1.5rem, 4vw, 2rem) !important;
    font-weight: 700 !important;
}

/* ---------- Progress Bars (for streaks) ---------- */
.stProgress > div > div > div > div {
    background: var(--primary);
    border-radius: var(--radius-full);
}

.stProgress > div > div {
    background: var(--surface-hover);
    border-radius: var(--radius-full);
    height: 0.5rem !important;
}

/* ---------- Tabs Navigation ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: var(--space-xs);
    background: var(--surface);
    padding: var(--space-xs);
    border-radius: var(--radius-lg);
    margin-bottom: var(--space-lg);
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;  /* Firefox */
    -ms-overflow-style: none;  /* IE/Edge */
}

.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
    display: none;  /* Chrome/Safari */
}

.stTabs [data-baseweb="tab"] {
    padding: var(--space-sm) var(--space-lg);
    background: transparent;
    border: none;
    border-radius: var(--radius-md);
    color: var(--text-secondary);
    font-weight: 500;
    white-space: nowrap;
    transition: all 0.2s ease;
    font-size: 0.95rem;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--surface-hover);
    color: var(--text-primary);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: var(--primary);
    color: white;
}

/* ---------- Alerts & Info Boxes ---------- */
.stAlert {
    padding: var(--space-md);
    border-radius: var(--radius-md);
    margin: var(--space-md) 0;
    border: 1px solid transparent;
}

/* Info alert (your archetype display) */
.stAlert.info {
    background: var(--primary-soft);
    border-color: var(--primary-light);
    color: var(--primary-dark);
}

/* Success alert */
.stAlert.success {
    background: #d1fae5;
    border-color: var(--success);
    color: #065f46;
}

/* Warning alert */
.stAlert.warning {
    background: #fed7aa;
    border-color: var(--warning);
    color: #92400e;
}

/* Error alert */
.stAlert.error {
    background: #fee2e2;
    border-color: var(--danger);
    color: #991b1b;
}

/* ---------- Expanders ---------- */
.streamlit-expanderHeader {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    font-weight: 600;
    color: var(--text-primary);
}

.streamlit-expanderContent {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 var(--radius-md) var(--radius-md);
    padding: var(--space-md);
}

/* ---------- Chat Messages ---------- */
.stChatMessage {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: var(--space-md);
    margin-bottom: var(--space-sm);
}

.stChatMessage[data-testid="user-message"] {
    background: var(--primary-soft);
    border-color: var(--primary-light);
}

/* Chat input */
.stChatInput > div > div > input {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-full);
    padding: var(--space-md) var(--space-lg);
    min-height: 52px;
    font-size: 1rem;
}

/* ---------- Plotly Charts ---------- */
.js-plotly-plot {
    background: var(--surface);
    border-radius: var(--radius-lg);
    padding: var(--space-sm);
    margin: var(--space-md) 0;
}

/* ---------- Dividers ---------- */
hr {
    margin: var(--space-xl) 0;
    border: none;
    border-top: 1px solid var(--border);
}

/* ---------- Code Blocks (for shareable insights) ---------- */
.stCode {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
}

.stCode > pre {
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
    font-size: 0.9rem !important;
}

/* ---------- Mobile-Specific Optimizations ---------- */
@media (max-width: 768px) {
    
    /* Adjust container padding */
    .block-container {
        padding: var(--space-md) var(--space-sm) !important;
    }
    
    /* Stack horizontal layouts */
    div.row-widget.stHorizontal {
        flex-direction: column;
        gap: var(--space-sm) !important;
    }
    
    div.row-widget.stHorizontal > div {
        width: 100%;
        min-width: 100%;
    }
    
    /* Make buttons full width and taller */
    .stButton > button {
        width: 100%;
        min-height: 52px;
        font-size: 1.1rem;
        padding: var(--space-sm) var(--space-md);
    }
    
    /* Improve text area on mobile */
    .stTextArea > div > div > textarea {
        min-height: 120px;
        font-size: 16px;  /* Prevents zoom on iOS */
    }
    
    /* Better spacing for metrics */
    .stMetric {
        padding: var(--space-sm);
        margin-bottom: var(--space-sm);
    }
    
    /* Adjust cards */
    .card {
        padding: var(--space-md);
        margin-bottom: var(--space-md);
    }
    
    /* Make tabs scrollable horizontally */
    .stTabs [data-baseweb="tab-list"] {
        flex-wrap: nowrap;
        justify-content: flex-start;
        padding: var(--space-xs);
    }
    
    /* Adjust tab padding */
    .stTabs [data-baseweb="tab"] {
        padding: var(--space-sm) var(--space-md);
        font-size: 0.9rem;
    }
    
    /* Reduce chart heights */
    .js-plotly-plot {
        height: auto !important;
        min-height: 250px;
    }
    
    /* Improve chat on mobile */
    .stChatInput > div > div > input {
        min-height: 56px;
        font-size: 16px;
    }
    
    /* Better spacing for journal entries */
    .stMarkdown h3 {
        margin-top: var(--space-lg);
    }
    
    /* Adjust divider spacing */
    hr {
        margin: var(--space-lg) 0;
    }
    
    /* Improve code block readability */
    .stCode > pre {
        font-size: 0.8rem !important;
        padding: var(--space-sm) !important;
    }
    
    /* Hide less important elements */
    .stProgress {
        margin-bottom: var(--space-sm);
    }
    
    /* Better touch scrolling */
    .main {
        -webkit-overflow-scrolling: touch;
    }
    
    /* Adjust caption text */
    .stCaption {
        font-size: 0.8rem;
    }
}

/* ---------- Small Phones (320px - 480px) ---------- */
@media (max-width: 480px) {
    
    .block-container {
        padding: var(--space-sm) !important;
    }
    
    .big-title {
        font-size: 2rem !important;
    }
    
    .subtitle {
        font-size: 0.95rem;
        margin-bottom: 20px;
    }
    
    h1 { font-size: 1.5rem; }
    h2 { font-size: 1.25rem; }
    h3 { font-size: 1.1rem; }
    
    p, .stMarkdown {
        font-size: 0.95rem;
    }
    
    .card {
        padding: var(--space-sm);
    }
    
    .stButton > button {
        min-height: 48px;
        font-size: 1rem;
    }
    
    /* Simplify cards */
    .card {
        box-shadow: none;
        border-width: 1px;
    }
    
    /* Reduce tab padding further */
    .stTabs [data-baseweb="tab"] {
        padding: var(--space-xs) var(--space-sm);
        font-size: 0.85rem;
    }
    
    /* Stack metrics */
    div.row-widget.stHorizontal {
        flex-direction: column;
    }
    
    /* Adjust charts */
    .js-plotly-plot {
        margin: var(--space-sm) 0;
        padding: var(--space-xs);
    }
}

/* ---------- Landscape Mode ---------- */
@media (orientation: landscape) and (max-height: 600px) {
    
    .stButton > button {
        min-height: 40px;
    }
    
    .block-container {
        padding-top: var(--space-sm) !important;
        padding-bottom: var(--space-sm) !important;
    }
    
    .big-title {
        font-size: 2rem !important;
        margin-bottom: 0;
    }
    
    .subtitle {
        margin-bottom: var(--space-sm);
    }
}

/* ---------- Dark Mode Support ---------- */
@media (prefers-color-scheme: dark) {
    
    .stApp {
        background: var(--background);
    }
    
    .card {
        background: var(--surface);
        border-color: var(--border);
    }
    
    .stTextArea > div > div > textarea {
        background: var(--surface);
        color: var(--text-primary);
        border-color: var(--border);
    }
    
    .stSelectbox > div > div > div {
        background: var(--surface);
        color: var(--text-primary);
    }
    
    .js-plotly-plot {
        background: var(--surface);
    }
    
    .stAlert.info {
        background: var(--primary-soft);
        color: var(--text-primary);
    }
    
    .streamlit-expanderHeader {
        background: var(--surface);
        border-color: var(--border);
    }
}

/* ---------- Loading States ---------- */
.stSpinner > div {
    border-color: var(--primary) transparent transparent transparent !important;
}

/* ---------- Tooltips ---------- */
[data-testid="stTooltip"] {
    background: var(--surface);
    color: var(--text-primary);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-xs) var(--space-sm);
    font-size: 0.875rem;
    box-shadow: var(--shadow-lg);
}

/* ---------- Custom Scrollbar ---------- */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--surface);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: var(--radius-full);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-tertiary);
}

/* ---------- Helper Classes (optional) ---------- */
.hide-mobile {
    @media (max-width: 768px) {
        display: none !important;
    }
}

.show-mobile {
    @media (min-width: 769px) {
        display: none !important;
    }
}

.text-center {
    text-align: center;
}

.text-left {
    text-align: left;
}

.text-right {
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# MOBILE DETECTION HELPER (Optional)
# ------------------------------------------------

def is_mobile():
    """Simple mobile detection based on session state"""
    return st.session_state.get('_mobile', False)

# Add mobile detection script
st.markdown("""
<script>
// Simple mobile detection
const isMobile = window.matchMedia("only screen and (max-width: 768px)").matches;
window.localStorage.setItem('isMobile', isMobile);
</script>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown("<div class='big-title'>🧠 MindMirror</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Understand your thoughts. Gain clarity.</div>", unsafe_allow_html=True)

# ------------------------------------------------
# INIT SYSTEMS
# ------------------------------------------------

initialize_journal(st.session_state)
initialize_checkins(st.session_state)
initialize_chat(st.session_state)

if "last_user_msg" not in st.session_state:
    st.session_state.last_user_msg = None

# ------------------------------------------------
# NAVIGATION
# ------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    ["Reflection", "Journal", "Daily Check-In", "AI Therapist"]
)

# =================================================
# REFLECTION
# =================================================

with tab1:

    st.markdown("### What's on your mind?")

    user_input = st.text_area(
        "",
        height=150 if not is_mobile() else 120,
        placeholder="Write freely. This is your private reflection space."
    )

    if st.button("Analyze Thought", type="primary"):

        if user_input.strip() == "":
            st.warning("Please write something first.")
            st.stop()

        with st.spinner("MindMirror is analyzing your thought..."):

            analysis = analyze_thought(user_input)

            distortions = detect_distortions(user_input)
            emotions = generate_emotion_profile(user_input)
            personality = build_personality_profile(user_input)

            clarity = build_clarity_report(
                emotions,
                distortions,
                personality
            )

            save_reflection(
                st.session_state,
                user_input,
                analysis,
                personality,
                emotions
            )

        # ------------------------------
        # ANALYSIS
        # ------------------------------

        st.markdown("## Reflection")

        st.markdown(
            f"<div class='card'>{analysis}</div>",
            unsafe_allow_html=True
        )

        # ------------------------------
        # CLARITY GAUGE
        # ------------------------------

        st.markdown("### Clarity Score")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=clarity["score"],
            title={'text': "Clarity"},
            gauge={
                'axis': {'range': [0,100]},
                'bar': {'color': "#2563eb"},
                'steps': [
                    {'range': [0,40], 'color': "#fee2e2"},
                    {'range': [40,70], 'color': "#fde68a"},
                    {'range': [70,100], 'color': "#bbf7d0"}
                ]
            }
        ))

        fig.update_layout(
            height=300 if not is_mobile() else 250,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(clarity["level"])
        st.write(clarity["summary"])

        # ------------------------------
        # EMOTION RADAR
        # ------------------------------

        st.markdown("### Emotional Signals")

        labels = list(emotions.keys())
        values = list(emotions.values())

        radar = go.Figure()

        radar.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            line_color='#2563eb',
            fillcolor='rgba(37, 99, 235, 0.3)'
        ))

        radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0,100],
                    color='#64748b'
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=False,
            height=400 if not is_mobile() else 300,
            margin=dict(l=40, r=40, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(radar, use_container_width=True)

        # ------------------------------
        # DISTORTIONS
        # ------------------------------

        st.markdown("### Cognitive Distortions")

        if distortions:
            # Display as pills/badges for better mobile experience
            distortion_html = "<div style='display: flex; flex-wrap: wrap; gap: 8px;'>"
            for d in distortions:
                distortion_html += f"<span style='background: var(--surface-hover); padding: 4px 12px; border-radius: 20px; font-size: 0.9rem; border: 1px solid var(--border);'>{d}</span>"
            distortion_html += "</div>"
            st.markdown(distortion_html, unsafe_allow_html=True)
        else:
            st.success("No major distortions detected.")

        # ------------------------------
        # PERSONALITY
        # ------------------------------

        st.markdown("### MindMirror Archetype")

        st.info(personality["archetype"])

        # ------------------------------
        # SHARE INSIGHT
        # ------------------------------

        share = build_share_block(analysis)

        if share:

            st.markdown("### Shareable Insight")

            # Make code block copyable and mobile-friendly
            st.code(share, language="text")

# =================================================
# JOURNAL
# =================================================

with tab2:

    st.markdown("## Reflection Journal")

    journal = get_journal(st.session_state)

    if not journal:
        st.info("You haven't created any reflections yet.")

    else:

        for entry in reversed(journal):

            # Create a collapsible card for each entry (better for mobile)
            with st.expander(f"📝 {entry['date']}"):
                st.markdown("**Thought**")
                st.write(entry["thought"])
                st.markdown("**Insight**")
                st.write(entry["analysis"])

# =================================================
# DAILY CHECK-IN
# =================================================

with tab3:

    st.markdown("## Daily Mind Check")

    # Create a card-like container
    st.markdown('<div class="card">', unsafe_allow_html=True)

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

    if st.button("Record Mood", type="primary"):
        record_checkin(st.session_state, mood)
        st.success("✅ Mood recorded!")

    st.markdown("</div>", unsafe_allow_html=True)

    # Streak display
    streak = get_streak(st.session_state)
    if streak > 0:
        st.markdown(f"""
        <div style='text-align: center; padding: var(--space-md); background: var(--surface); border-radius: var(--radius-lg); border: 1px solid var(--border);'>
            <div style='font-size: 3rem;'>🔥</div>
            <div style='font-size: 2rem; font-weight: 700; color: var(--primary);'>{streak}</div>
            <div style='color: var(--text-secondary);'>day streak</div>
        </div>
        """, unsafe_allow_html=True)

    checkins = get_checkins(st.session_state)

    if checkins:

        st.markdown("### Mood History")

        # Create a simple table for mood history
        mood_data = []
        for c in reversed(checkins[-7:]):  # Last 7 days
            mood_data.append({"Date": c['date'][5:], "Mood": c['mood']})

        if mood_data:
            df = pd.DataFrame(mood_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

# =================================================
# AI THERAPIST
# =================================================

with tab4:

    st.markdown("## AI Therapist")

    # Chat container with fixed height for better mobile experience
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.chat_history:

            if msg["role"] == "system":
                continue

            with st.chat_message(msg["role"]):
                st.write(msg["content"])

# ------------------------------------------------
# CHAT INPUT (Outside tabs for global access)
# ------------------------------------------------

user_msg = st.chat_input("Share what's on your mind...")

if user_msg and user_msg != st.session_state.last_user_msg:

    st.session_state.last_user_msg = user_msg

    add_user_message(st.session_state, user_msg)

    with st.spinner("Thinking..."):
        reply = generate_response(st.session_state)

    add_assistant_message(st.session_state, reply)

    st.rerun()

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown("---")

st.markdown("""
<div style='text-align: center; color: var(--text-tertiary); font-size: 0.8rem; padding: var(--space-md);'>
    MindMirror • A reflection tool for clarity<br>
    Not a substitute for professional mental health care.
</div>
""", unsafe_allow_html=True)