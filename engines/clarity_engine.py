"""
MindMirror Clarity Engine
-------------------------

Combines emotional signals, cognitive distortions,
and personality traits to generate a psychological
clarity score and insight summary.
"""


# ----------------------------------------
# CLARITY SCORE
# ----------------------------------------

def calculate_clarity_score(emotions, distortions, personality):

    """
    Calculate overall mental clarity score.
    """

    score = 100

    # Emotional penalties (strongest impact)
    score -= emotions.get("Anxiety", 0) * 0.35
    score -= emotions.get("Fear", 0) * 0.35
    score -= emotions.get("Sadness", 0) * 0.25
    score -= emotions.get("Self Doubt", 0) * 0.35

    # Distortion penalties
    score -= len(distortions) * 7

    # Personality bonuses
    traits = personality.get("traits", {})

    score += traits.get("Self-Aware", 0) * 0.25
    score += traits.get("Growth-Oriented", 0) * 0.25

    # Clamp range
    score = max(10, min(100, int(score)))

    return score


# ----------------------------------------
# CLARITY LEVEL
# ----------------------------------------

def determine_clarity_level(score):

    """
    Convert clarity score into interpretation.
    """

    if score >= 80:
        return "High Clarity"

    if score >= 60:
        return "Moderate Clarity"

    if score >= 40:
        return "Low Clarity"

    return "Mental Fog"


# ----------------------------------------
# DOMINANT EMOTION
# ----------------------------------------

def get_dominant_emotion(emotions):

    if not emotions:
        return None

    return max(emotions, key=emotions.get)


# ----------------------------------------
# PSYCHOLOGICAL SUMMARY
# ----------------------------------------

def generate_psychological_summary(emotions, distortions, personality):

    """
    Generate a more human psychological insight summary.
    """

    dominant_emotion = get_dominant_emotion(emotions)

    archetype = personality.get("archetype", "Exploring Mind")

    distortion_count = len(distortions)

    summary = f"""
Your current thought pattern appears to be strongly influenced by **{dominant_emotion}**.

When this emotion becomes dominant, the mind can start interpreting
situations through emotional pressure rather than clear perspective.

Your personality pattern currently aligns with **{archetype}**, which
suggests you naturally tend to analyze and explore your internal experiences.

MindMirror detected **{distortion_count} cognitive distortion patterns** in your thinking.
These distortions can make thoughts feel more convincing than they actually are.

With a bit of reflection and emotional distance, your perspective may
naturally regain clarity.
"""

    return summary.strip()


# ----------------------------------------
# BUILD REPORT
# ----------------------------------------

def build_clarity_report(emotions, distortions, personality):

    """
    Build final clarity report used by the UI.
    """

    score = calculate_clarity_score(
        emotions,
        distortions,
        personality
    )

    level = determine_clarity_level(score)

    summary = generate_psychological_summary(
        emotions,
        distortions,
        personality
    )

    return {
        "score": score,
        "level": level,
        "summary": summary
    }