"""
MindMirror Cognitive Distortion Detector
----------------------------------------

Detects common cognitive distortions from user thoughts.

These distortions are simplified patterns based on
Cognitive Behavioral Therapy (CBT).

Used by MindMirror to highlight thinking biases.
"""

import re


DISTORTION_PATTERNS = {

    "Catastrophizing": [
        r"everything (is|will be) ruined",
        r"this is the worst",
        r"my life is over",
        r"nothing will work",
        r"this will never work",
        r"disaster",
        r"i can't handle this"
    ],

    "Overgeneralization": [
        r"\balways\b",
        r"\bnever\b",
        r"\bevery time\b",
        r"\bnothing ever\b",
        r"\beveryone\b"
    ],

    "Mind Reading": [
        r"they think",
        r"everyone thinks",
        r"they must think",
        r"people think",
        r"they probably think"
    ],

    "Emotional Reasoning": [
        r"i feel like",
        r"it feels like",
        r"because i feel",
        r"my gut says"
    ],

    "Black and White Thinking": [
        r"\beither\b",
        r"\bcompletely\b",
        r"\btotally\b",
        r"\bperfect\b",
        r"\bfailure\b",
        r"all or nothing"
    ],

    "Self-Blame": [
        r"it's my fault",
        r"i ruined",
        r"i always mess up",
        r"i'm the problem",
        r"this is because of me"
    ],

    "Fortune Telling": [
        r"this will end badly",
        r"i know it will fail",
        r"it's going to go wrong"
    ],

    "Personalization": [
        r"they are upset because of me",
        r"this happened because of me"
    ]
}


def detect_distortions(text: str):
    """
    Detect cognitive distortions within a thought.
    """

    text = text.lower()

    detected = []

    for distortion, patterns in DISTORTION_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, text):

                detected.append(distortion)
                break

    # remove duplicates
    detected = list(set(detected))

    return detected