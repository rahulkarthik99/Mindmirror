"""
MindMirror Reflection Journal
-----------------------------

Stores, retrieves, and analyzes user reflections.

Used for:
• journaling
• emotional trend tracking
• detecting repeated thought patterns
"""

from datetime import datetime


# ------------------------------------------------
# INITIALIZE JOURNAL
# ------------------------------------------------

def initialize_journal(session_state):
    """
    Ensure journal exists in session state.
    """

    if "journal" not in session_state:
        session_state.journal = []


# ------------------------------------------------
# SAVE REFLECTION
# ------------------------------------------------

def save_reflection(session_state, thought, analysis, personality=None, emotions=None):
    """
    Store a reflection entry.
    """

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "thought": thought,
        "analysis": analysis,
        "personality": personality or {},
        "emotions": emotions or {}
    }

    session_state.journal.append(entry)


# ------------------------------------------------
# GET JOURNAL
# ------------------------------------------------

def get_journal(session_state):
    """
    Return all journal entries.
    """

    return session_state.journal


# ------------------------------------------------
# GET RECENT ENTRIES
# ------------------------------------------------

def get_recent_entries(session_state, limit=5):
    """
    Return most recent reflections.
    """

    return session_state.journal[-limit:]


# ------------------------------------------------
# CLEAR JOURNAL
# ------------------------------------------------

def clear_journal(session_state):
    """
    Reset journal history.
    """

    session_state.journal = []


# ------------------------------------------------
# DETECT RECURRING THEMES
# ------------------------------------------------

def detect_thought_loops(session_state):
    """
    Detect recurring emotional themes.
    """

    journal = session_state.journal

    emotion_counts = {}

    for entry in journal:

        emotions = entry.get("emotions", {})

        for emotion, score in emotions.items():

            if score > 40:

                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

    return emotion_counts


# ------------------------------------------------
# JOURNAL STATISTICS
# ------------------------------------------------

def get_journal_stats(session_state):
    """
    Generate simple statistics from reflections.
    """

    journal = session_state.journal

    total_entries = len(journal)

    if total_entries == 0:
        return {
            "entries": 0,
            "dominant_emotion": None
        }

    emotion_counts = {}

    for entry in journal:

        emotions = entry.get("emotions", {})

        for emotion, score in emotions.items():

            if score > 30:

                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

    dominant = None

    if emotion_counts:
        dominant = max(emotion_counts, key=emotion_counts.get)

    return {
        "entries": total_entries,
        "dominant_emotion": dominant
    }