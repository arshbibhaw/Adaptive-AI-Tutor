"""
Topic planner service.

Generates topic breakdown from a raw topic string (non-document mode).

============================================================
PLACEHOLDER — LLM provider not yet configured.
============================================================
TODO: When the LLM provider is selected, replace the static
topic breakdown with an LLM-powered concept extraction call.
============================================================
"""

import logging
import uuid

logger = logging.getLogger(__name__)


async def plan_topic(
    topic: str,
    learner_level: str = "beginner",
    duration_minutes: int = 20,
    language: str = "en",
) -> dict:
    """
    Break down a topic into a structured concept hierarchy.

    ============================================================
    PLACEHOLDER: Returns a static structure for the given topic.
    Replace with LLM call when provider is configured.
    ============================================================
    """
    logger.warning(
        "PLACEHOLDER: Using static topic breakdown. Configure LLM_API_KEY for dynamic planning."
    )

    # Generate a reasonable placeholder breakdown
    concepts = _generate_placeholder_concepts(topic, duration_minutes)

    return {
        "topic": topic,
        "concepts": concepts,
        "prerequisites": [],
        "estimated_duration": duration_minutes,
        "language": language,
        "level": learner_level,
    }


def _generate_placeholder_concepts(topic: str, duration_minutes: int) -> list[dict]:
    """Generate placeholder concepts based on topic and time."""
    # Calculate number of concepts based on time
    num_concepts = max(2, min(duration_minutes // 4, 10))

    concepts = []
    for i in range(num_concepts):
        concepts.append({
            "id": f"c{i + 1}",
            "name": f"{topic} — Concept {i + 1}",
            "order": i + 1,
            "estimated_minutes": duration_minutes // num_concepts,
            "prerequisites": [f"c{i}"] if i > 0 else [],
        })

    return concepts
