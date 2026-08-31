"""
Learning report service.

Generates final learning reports with scores, strong/weak concepts,
misconceptions, revision recommendations, and next topic suggestions.

============================================================
PLACEHOLDER — LLM provider not yet configured.
============================================================
TODO: When the LLM provider is selected, enhance report
generation with LLM-powered analysis for:
  - Personalized learning insights
  - Specific revision recommendations
  - Next topic suggestions based on curriculum knowledge
============================================================
"""

import logging

from backend.app.schemas.progress import LearningReportResponse

logger = logging.getLogger(__name__)


async def generate_learning_report(
    session_id: str,
    concepts_covered: list[str],
    strong_concepts: list[str],
    weak_concepts: list[str],
    misconceptions: list[str],
    total_questions: int,
    correct_answers: int,
    topic: str = "",
) -> LearningReportResponse:
    """
    Generate a comprehensive learning report for a completed session.

    ============================================================
    PLACEHOLDER: Returns a structured report with basic analysis.
    Replace with LLM-enhanced insights when provider is configured.
    ============================================================
    """
    logger.info("Generating learning report for session %s.", session_id)

    score = correct_answers / total_questions if total_questions > 0 else 0.0

    # Generate revision recommendations
    revision_recommendations = []
    for concept in weak_concepts:
        revision_recommendations.append(
            f"Review {concept} — focus on the fundamental principles."
        )
    for misconception in misconceptions:
        revision_recommendations.append(
            f"Address misconception: {misconception}"
        )

    # Suggest next topic
    next_topic = _suggest_next_topic(topic, strong_concepts, weak_concepts)

    return LearningReportResponse(
        session_id=session_id,
        total_questions=total_questions,
        correct_answers=correct_answers,
        score=round(score, 2),
        strong_concepts=strong_concepts,
        weak_concepts=weak_concepts,
        misconceptions=misconceptions,
        revision_recommendations=revision_recommendations,
        next_topic=next_topic,
    )


def _suggest_next_topic(
    current_topic: str,
    strong_concepts: list[str],
    weak_concepts: list[str],
) -> str | None:
    """
    Suggest the next topic to study.

    ============================================================
    PLACEHOLDER: Returns a generic suggestion.
    Replace with curriculum-aware suggestion when LLM is configured.
    ============================================================
    """
    if weak_concepts:
        return f"Revision: {weak_concepts[0]}"
    elif current_topic:
        return f"Advanced {current_topic}"
    return None
