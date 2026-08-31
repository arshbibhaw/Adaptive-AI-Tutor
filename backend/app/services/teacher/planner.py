"""
Lesson planner service.

Converts topic/material into a structured LessonPlan.

============================================================
PLACEHOLDER — LLM provider not yet configured.
============================================================
TODO: When the LLM provider is selected, replace the static
lesson plan generation with an LLM-powered planning call that:
  - Analyzes retrieved context / topic breakdown
  - Orders concepts logically with prerequisites
  - Allocates time to each concept
  - Decides checkpoints, examples, and visual types
  - Produces a structured LessonPlan JSON
============================================================
"""

import logging
import uuid

from backend.app.schemas.lesson import LessonPlan, LessonSegment
from backend.app.services.teacher.personalization import (
    get_personalization_context,
    get_time_config,
)
from backend.app.services.teacher.topic_planner import plan_topic

logger = logging.getLogger(__name__)


async def generate_lesson_plan(
    topic: str | None = None,
    document_outline: dict | None = None,
    retrieved_context: list[dict] | None = None,
    learner_level: str = "beginner",
    language: str = "en",
    duration_minutes: int = 20,
    goal: str | None = None,
) -> LessonPlan:
    """
    Generate a structured LessonPlan from a topic or document context.

    ============================================================
    PLACEHOLDER: Generates a static lesson plan structure.
    Replace with LLM call when provider is configured.
    ============================================================
    """
    logger.warning(
        "PLACEHOLDER: Using static lesson plan. Configure LLM_API_KEY for dynamic planning."
    )

    personalization = get_personalization_context(learner_level, language, goal)
    time_config = get_time_config(duration_minutes)

    # Determine concepts either from document outline or topic
    if document_outline and document_outline.get("sections"):
        concepts = [
            s.get("heading", f"Section {i + 1}")
            for i, s in enumerate(document_outline["sections"])
        ]
    elif topic:
        topic_plan = await plan_topic(topic, learner_level, duration_minutes, language)
        concepts = [c["name"] for c in topic_plan.get("concepts", [])]
    else:
        concepts = ["Introduction"]

    # Limit concepts by time config
    max_concepts = time_config["max_concepts"]
    concepts = concepts[:max_concepts]

    if not concepts:
        concepts = ["General Overview"]

    # Build lesson segments
    minutes_per_concept = max(1, duration_minutes // len(concepts))
    segments = []

    for i, concept in enumerate(concepts):
        segment_id = f"s{i + 1}"
        is_checkpoint = (i + 1) % max(1, len(concepts) // max(1, time_config["checkpoints"])) == 0

        segments.append(LessonSegment(
            id=segment_id,
            concept=concept,
            minutes=minutes_per_concept,
            explanation=f"Explanation of {concept} for {learner_level} level.",
            example=f"Example illustrating {concept}.",
            visual_type=_suggest_visual_type(concept),
            checkpoint=is_checkpoint or (i == len(concepts) - 1),
        ))

    title = topic or document_outline.get("title", "Lesson") if document_outline else "Lesson"

    return LessonPlan(
        title=title,
        duration_minutes=duration_minutes,
        language=language,
        learner_level=learner_level,
        segments=segments,
    )


def _suggest_visual_type(concept: str) -> str:
    """
    Suggest a visual type based on the concept name.

    Subject-aware visual selection per Team 4 spec.
    """
    concept_lower = concept.lower()

    # Math keywords
    if any(kw in concept_lower for kw in ["equation", "formula", "calculus", "algebra", "math"]):
        return "equation"

    # Physics keywords
    if any(kw in concept_lower for kw in ["force", "energy", "voltage", "current", "physics", "ohm"]):
        return "diagram"

    # Biology keywords
    if any(kw in concept_lower for kw in ["cell", "dna", "protein", "biology", "organ"]):
        return "diagram"

    # History keywords
    if any(kw in concept_lower for kw in ["history", "war", "century", "empire", "revolution"]):
        return "timeline"

    # Programming keywords
    if any(kw in concept_lower for kw in ["code", "function", "algorithm", "programming", "python"]):
        return "code"

    # AI/ML keywords
    if any(kw in concept_lower for kw in ["neural", "model", "training", "ai", "machine learning"]):
        return "graph"

    return "diagram"
