"""
MindMirror Thought Analyzer
---------------------------

Responsible for:
1. Constructing the structured psychological reflection prompt
2. Sending analysis request to Groq LLM
3. Returning structured reflection text

Used by mindmirror_app.py
"""

import os
from groq import Groq
from dotenv import load_dotenv

# ------------------------------------------------
# ENVIRONMENT SETUP
# ------------------------------------------------

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ------------------------------------------------
# PROMPT BUILDER
# ------------------------------------------------

def build_prompt(user_text: str) -> str:
    """
    Construct the psychological reflection prompt.
    """

    # Prevent extremely long input from degrading responses
    user_text = user_text.strip()[:1200]

    prompt = f"""
You are MindMirror — a thoughtful psychological reflection assistant.

Your goal is to help the user understand their thoughts with clarity,
emotional intelligence, and compassionate insight.

The user is reflecting on the following thought:

"{user_text}"

Write a thoughtful analysis using the sections below.

ROOT CAUSE
Identify the emotional or situational trigger behind these thoughts.

EMOTIONAL STATE
Describe the emotions the user may currently be experiencing.

HIDDEN FEAR
Identify the deeper fear, insecurity, or uncertainty driving these thoughts.

CORE PROBLEM
Explain the deeper psychological issue beneath the surface.

ASSUMPTIONS
Point out beliefs the user might be making without solid evidence.

EXAGGERATIONS
Identify where the mind might be magnifying or catastrophizing events.

EMOTIONAL REASONING
Explain where emotions may be mistaken for facts.

REALITY CHECK
Compare these thoughts with objective reality.

OBJECTIVE TRUTH
State the factual situation stripped of emotional interpretation.

REFRAME
Offer a healthier and more constructive interpretation.

KEY REALIZATION
Write one clear and powerful insight the user should understand.

IMMEDIATE STEPS
Suggest 3 small practical actions the user can take today.

SHORT TERM PLAN
Provide guidance for the next few days or weeks.

MINDSET SHIFT
Describe a deeper long-term shift in thinking that could help.

Writing style rules:

• Use a calm, compassionate tone  
• Write like a thoughtful mentor, not a clinical therapist  
• Avoid robotic or academic language  
• Avoid repeating the section titles in sentences  
• Keep explanations insightful but readable  
• Do not be overly verbose
"""

    return prompt


# ------------------------------------------------
# THOUGHT ANALYSIS
# ------------------------------------------------

def analyze_thought(user_text: str) -> str:
    """
    Send the user's thought to the LLM for analysis.
    """

    prompt = build_prompt(user_text)

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": """
You are MindMirror, an emotionally intelligent reflection assistant.

You help users understand their thoughts clearly and compassionately.

Your responses should feel insightful, calm, and psychologically aware.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,
            max_tokens=1500
        )

        result = response.choices[0].message.content.strip()

        return result

    except Exception as e:

        return f"Error analyzing thought: {str(e)}"