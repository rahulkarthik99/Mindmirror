"""
MindMirror Daily Check-In System
--------------------------------

Allows users to log emotional state each day.

Tracks:
• daily mood logs
• real consecutive streaks
• emotional trends
"""

from datetime import datetime, timedelta


# ----------------------------------------
# INITIALIZE
# ----------------------------------------

def initialize_checkins(session_state):

    if "daily_checkins" not in session_state:
        session_state.daily_checkins = []

    if "streak" not in session_state:
        session_state.streak = 0


# ----------------------------------------
# RECORD CHECK-IN
# ----------------------------------------

def record_checkin(session_state, mood):

    today = datetime.now().strftime("%Y-%m-%d")

    # prevent duplicate check-ins for same day
    for entry in session_state.daily_checkins:
        if entry["date"] == today:
            entry["mood"] = mood
            update_streak(session_state)
            return

    entry = {
        "date": today,
        "mood": mood
    }

    session_state.daily_checkins.append(entry)

    update_streak(session_state)


# ----------------------------------------
# UPDATE STREAK
# ----------------------------------------

def update_streak(session_state):

    if not session_state.daily_checkins:
        session_state.streak = 0
        return

    dates = sorted(
        [datetime.strptime(e["date"], "%Y-%m-%d") for e in session_state.daily_checkins]
    )

    streak = 1

    for i in range(len(dates) - 1, 0, -1):

        if dates[i] - dates[i - 1] == timedelta(days=1):
            streak += 1
        else:
            break

    session_state.streak = streak


# ----------------------------------------
# GET CHECKINS
# ----------------------------------------

def get_checkins(session_state):

    return session_state.daily_checkins


# ----------------------------------------
# GET STREAK
# ----------------------------------------

def get_streak(session_state):

    return session_state.streak


# ----------------------------------------
# MOOD STATISTICS
# ----------------------------------------

def get_mood_statistics(session_state):

    moods = {}

    for entry in session_state.daily_checkins:

        mood = entry["mood"]

        moods[mood] = moods.get(mood, 0) + 1

    if not moods:
        return {
            "dominant_mood": None,
            "total_entries": 0
        }

    dominant = max(moods, key=moods.get)

    return {
        "dominant_mood": dominant,
        "total_entries": len(session_state.daily_checkins)
    }