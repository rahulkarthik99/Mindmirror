"""
MindMirror Engines Package
==========================

Contains all core processing engines for thought analysis,
emotion detection, and cognitive reflection.
"""

# Export all engine modules
from . import (
    thought_analyzer,
    distortion_detector,
    emotion_engine,
    personality_mapper,
    clarity_engine,
    reflection_journal,
    daily_checkin,
    therapist_chat,
    insight_share_engine
)

__all__ = [
    'thought_analyzer',
    'distortion_detector',
    'emotion_engine',
    'personality_mapper',
    'clarity_engine',
    'reflection_journal',
    'daily_checkin',
    'therapist_chat',
    'insight_share_engine'
]

# Version for engines package
__version__ = "1.0.0"