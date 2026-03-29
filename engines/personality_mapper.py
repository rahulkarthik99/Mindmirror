"""
MindMirror Personality Mapper
-----------------------------

Infers personality tendencies from the user's thought patterns.

This is not a clinical personality assessment,
but a reflective personality signal detector
used to generate MindMirror archetypes.
"""

import re


TRAIT_PATTERNS = {

    "Analytical": [
        r"think",
        r"analyze",
        r"understand",
        r"figure out",
        r"why does",
        r"why do i"
    ],

    "Self-Aware": [
        r"i realize",
        r"i notice",
        r"i understand myself",
        r"i'm aware",
        r"i see that"
    ],

    "Anxious": [
        r"worried",
        r"overthinking",
        r"anxious",
        r"panic",
        r"can't stop thinking"
    ],

    "Self-Doubting": [
        r"not good enough",
        r"i will fail",
        r"i can't do this",
        r"i'm not capable",
        r"i'm a failure"
    ],

    "Growth-Oriented": [
        r"improve",
        r"change",
        r"learn",
        r"grow",
        r"be better"
    ],

    "Emotionally Sensitive": [
        r"hurt",
        r"feel deeply",
        r"sensitive",
        r"heartbroken",
        r"emotionally"
    ]
}


def detect_traits(text: str):
    """
    Detect personality signals using pattern matching.
    """

    text = text.lower()

    scores = {trait: 0 for trait in TRAIT_PATTERNS.keys()}

    for trait, patterns in TRAIT_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, text):
                scores[trait] += 1

    return normalize_scores(scores)


def normalize_scores(raw_scores):
    """
    Convert raw counts into a 0–100 scale.
    """

    normalized = {}

    for trait, value in raw_scores.items():

        score = min(value * 25, 100)

        normalized[trait] = score

    return normalized


def determine_archetype(scores):
    """
    Determine psychological archetype.
    """

    if scores["Analytical"] >= 50 and scores["Self-Aware"] >= 50:
        return "The Reflective Thinker"

    if scores["Anxious"] >= 50 and scores["Self-Doubting"] >= 50:
        return "The Overthinking Mind"

    if scores["Growth-Oriented"] >= 50:
        return "The Growth Seeker"

    if scores["Emotionally Sensitive"] >= 50:
        return "The Deep Feeler"

    return "The Exploring Mind"


def build_personality_profile(text: str):
    """
    Build full personality profile.
    """

    trait_scores = detect_traits(text)

    archetype = determine_archetype(trait_scores)

    return {
        "archetype": archetype,
        "traits": trait_scores
    }