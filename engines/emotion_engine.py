"""
MindMirror Emotional Intelligence Engine
----------------------------------------

Detects emotional signals from user thoughts and
converts them into normalized emotional metrics.

Used for:
• emotion charts
• clarity scoring
• psychological insights
"""

import re


EMOTION_PATTERNS = {

    "Anxiety": [
        r"worried",
        r"anxious",
        r"nervous",
        r"panic",
        r"overthinking",
        r"can't stop thinking",
        r"what if"
    ],

    "Sadness": [
        r"sad",
        r"lonely",
        r"depressed",
        r"empty",
        r"hopeless",
        r"hurt",
        r"heartbroken"
    ],

    "Anger": [
        r"angry",
        r"frustrated",
        r"hate",
        r"annoyed",
        r"irritated"
    ],

    "Fear": [
        r"afraid",
        r"scared",
        r"terrified",
        r"fear",
        r"panic"
    ],

    "Self Doubt": [
        r"not good enough",
        r"i'm a failure",
        r"worthless",
        r"useless",
        r"i can't do anything right"
    ],

    "Hope": [
        r"hope",
        r"maybe things will",
        r"improve",
        r"change",
        r"growth"
    ]
}


def detect_emotions(text: str):
    """
    Detect emotional signals using pattern matching.
    """

    text = text.lower()

    scores = {emotion: 0 for emotion in EMOTION_PATTERNS.keys()}

    for emotion, patterns in EMOTION_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, text):
                scores[emotion] += 1

    return scores


def normalize_scores(raw_scores):
    """
    Convert raw emotion counts into 0–100 scale.
    """

    normalized = {}

    for emotion, value in raw_scores.items():

        score = min(value * 25, 100)

        normalized[emotion] = score

    return normalized


def generate_emotion_profile(text: str):
    """
    Main function used by the app.
    """

    raw_scores = detect_emotions(text)

    normalized_scores = normalize_scores(raw_scores)

    return normalized_scores


def generate_clarity_score(emotion_scores):
    """
    Estimate mental clarity based on emotional load.
    """

    negative_load = (
        emotion_scores["Anxiety"]
        + emotion_scores["Sadness"]
        + emotion_scores["Fear"]
        + emotion_scores["Self Doubt"]
    )

    negative_load = negative_load / 4

    clarity = max(10, int(100 - negative_load))

    return clarity