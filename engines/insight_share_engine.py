"""
MindMirror Insight Share Engine
-------------------------------

Extracts meaningful insights from AI analysis
and converts them into shareable quotes.
"""


import re


# ------------------------------------------------
# EXTRACT KEY INSIGHT
# ------------------------------------------------

def extract_key_insight(analysis_text: str):
    """
    Extract the KEY REALIZATION insight
    from the analysis output.
    """

    if not analysis_text:
        return None

    lines = analysis_text.split("\n")

    capture = False
    insight_lines = []

    for line in lines:

        line = line.strip()

        if "KEY REALIZATION" in line.upper():
            capture = True
            continue

        if capture:

            # stop when another section starts
            if line == "" or line.isupper():
                break

            # remove bullet points
            line = re.sub(r"^[•\-–]", "", line).strip()

            # skip meta questions
            if "?" in line:
                continue

            # skip meta instruction text
            if "insight the user should take away" in line.lower():
                continue

            insight_lines.append(line)

    if not insight_lines:
        return None

    # return first clean sentence
    insight = insight_lines[0]

    return clean_sentence(insight)


# ------------------------------------------------
# CLEAN SENTENCE
# ------------------------------------------------

def clean_sentence(text):

    text = text.strip()

    # remove trailing punctuation noise
    text = re.sub(r"\s+", " ", text)

    if len(text) > 220:
        text = text[:220]

    return text


# ------------------------------------------------
# GENERATE SHARE TEXT
# ------------------------------------------------

def generate_share_text(insight: str):

    """
    Generate formatted share block.
    """

    if not insight:
        return None

    return f"""🧠 MindMirror Insight

"{insight}"

Reflect. Understand. Grow.

#MindMirror #SelfReflection #MentalClarity
"""


# ------------------------------------------------
# OPTIONAL SOCIAL VERSION
# ------------------------------------------------

def generate_social_post(insight):

    if not insight:
        return None

    return f"""
"{insight}"

— MindMirror
"""


# ------------------------------------------------
# BUILD SHARE BLOCK
# ------------------------------------------------

def build_share_block(analysis_text):

    insight = extract_key_insight(analysis_text)

    if not insight:
        return None

    return generate_share_text(insight)