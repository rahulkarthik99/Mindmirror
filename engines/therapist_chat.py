"""
MindMirror AI Therapist Chat
----------------------------

Conversational reflection assistant designed to help users
explore thoughts, emotions, fears, and cognitive patterns.

The assistant behaves like a thoughtful reflection partner,
not a clinical therapist.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ----------------------------------------
# INITIALIZE CHAT
# ----------------------------------------

def initialize_chat(session_state):

    if "chat_history" not in session_state:

        session_state.chat_history = [

            {
                "role": "system",
                "content": """
You are MindMirror — a thoughtful psychological reflection partner.

Your goal is to help users understand their thoughts
with clarity and emotional awareness.

Your personality:
• calm
• curious
• insightful
• compassionate

You are NOT a clinical therapist.

Your role is to help users explore their inner world
through reflection and thoughtful questioning.

Conversation principles:

• Avoid generic therapy clichés
• Avoid robotic or academic language
• Avoid one-line responses
• Keep responses between 4–6 sentences
• Speak like a thoughtful mentor

Always follow this response flow:

1. Reflect the emotion the user might be experiencing
2. Offer a deeper psychological observation
3. Ask a thoughtful follow-up question

Never talk about news, politics, or unrelated topics.

Focus only on the user's thoughts and emotional experience.
"""
            },

            {
                "role": "assistant",
                "content": "I'm here to help you understand your thoughts a little more clearly. What's been on your mind lately?"
            }

        ]

    # Track last processed message to avoid duplicates
    if "last_user_msg" not in session_state:
        session_state.last_user_msg = None


# ----------------------------------------
# ADD USER MESSAGE
# ----------------------------------------

def add_user_message(session_state, message):

    message = message.strip()

    session_state.chat_history.append(
        {
            "role": "user",
            "content": message
        }
    )


# ----------------------------------------
# ADD ASSISTANT MESSAGE
# ----------------------------------------

def add_assistant_message(session_state, message):

    session_state.chat_history.append(
        {
            "role": "assistant",
            "content": message
        }
    )


# ----------------------------------------
# TRIM CHAT HISTORY
# ----------------------------------------

def trim_history(session_state, max_messages=16):

    """
    Prevent long conversations from degrading model quality.
    Keeps system prompt + most recent messages.
    """

    history = session_state.chat_history

    if len(history) > max_messages:

        system_prompt = history[0]

        recent_messages = history[-(max_messages - 1):]

        session_state.chat_history = [system_prompt] + recent_messages


# ----------------------------------------
# GENERATE RESPONSE
# ----------------------------------------

def generate_response(session_state):

    try:

        trim_history(session_state)

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=session_state.chat_history,

            temperature=0.85,
            max_tokens=550
        )

        reply = response.choices[0].message.content.strip()

        return reply

    except Exception as e:

        return f"Error generating response: {str(e)}"