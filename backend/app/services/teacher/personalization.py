"""
Personalization service.

Adapts lesson content based on learner level, language, and preferences.
"""

import logging

logger = logging.getLogger(__name__)


def get_personalization_context(
    learner_level: str,
    language: str,
    goals: str | None = None,
    preferences: dict | None = None,
) -> dict:
    """
    Generate personalization context to guide the Teacher Agent.

    Returns a dict of personalization parameters that influence
    explanation style, depth, examples, and vocabulary.
    """
    level_config = _get_level_config(learner_level)

    return {
        "level": learner_level,
        "language": language,
        "goals": goals or "general understanding",
        "style": level_config["style"],
        "depth": level_config["depth"],
        "use_analogies": level_config["use_analogies"],
        "use_technical_terms": level_config["use_technical_terms"],
        "use_math": level_config["use_math"],
        "example_type": level_config["example_type"],
        "preferences": preferences or {},
    }


def _get_level_config(level: str) -> dict:
    """Return configuration for a given learner level per Team 2 spec."""
    configs = {
        "beginner": {
            "style": "simple, conversational, encouraging",
            "depth": "fundamentals only",
            "use_analogies": True,
            "use_technical_terms": False,
            "use_math": False,
            "example_type": "everyday analogies",
        },
        "intermediate": {
            "style": "balanced, clear with some technical language",
            "depth": "concepts with practical applications",
            "use_analogies": True,
            "use_technical_terms": True,
            "use_math": True,
            "example_type": "practical, real-world examples",
        },
        "advanced": {
            "style": "technical, precise, scholarly",
            "depth": "full technical depth with proofs/derivations where appropriate",
            "use_analogies": False,
            "use_technical_terms": True,
            "use_math": True,
            "example_type": "implementation-level or research-level examples",
        },
    }
    return configs.get(level, configs["beginner"])


def get_time_config(duration_minutes: int) -> dict:
    """
    Return time allocation guidance based on available duration.

    Per Team 2 spec: 5-min, 20-min, 60-min, multi-day modes.
    """
    if duration_minutes <= 5:
        return {
            "mode": "quick",
            "max_concepts": 2,
            "explanation_depth": "brief",
            "checkpoints": 1,
            "include_assessment": False,
        }
    elif duration_minutes <= 20:
        return {
            "mode": "standard",
            "max_concepts": 5,
            "explanation_depth": "moderate",
            "checkpoints": 3,
            "include_assessment": True,
        }
    elif duration_minutes <= 60:
        return {
            "mode": "deep",
            "max_concepts": 10,
            "explanation_depth": "thorough",
            "checkpoints": 5,
            "include_assessment": True,
        }
    else:
        return {
            "mode": "extended",
            "max_concepts": 20,
            "explanation_depth": "comprehensive",
            "checkpoints": 8,
            "include_assessment": True,
        }
