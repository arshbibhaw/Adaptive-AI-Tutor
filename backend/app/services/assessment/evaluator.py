"""
Answer evaluator service.

Evaluates student answers: correct, partially correct, incorrect, off-topic.
Returns score + explanation + confidence.

============================================================
PLACEHOLDER — LLM provider not yet configured.
============================================================
TODO: When the LLM provider is selected, replace static
evaluation with LLM-powered evaluation that:
  - Understands natural language answers
  - Detects partial correctness
  - Provides meaningful feedback
  - Assigns confidence scores
============================================================
"""

import logging

from backend.app.schemas.evaluation import StudentEvaluation

logger = logging.getLogger(__name__)


async def evaluate_answer(
    question_id: str,
    student_answer: str,
    correct_answer: str | None = None,
    concept: str = "",
    question_type: str = "mcq",
    difficulty: str = "medium",
) -> StudentEvaluation:
    """
    Evaluate a student's answer.

    ============================================================
    PLACEHOLDER: Uses simple string matching for MCQs and
    always returns partially correct for open-ended questions.
    Replace with LLM-powered evaluation when configured.
    ============================================================
    """
    logger.warning(
        "PLACEHOLDER: Using basic evaluation. Configure LLM_API_KEY for LLM-powered evaluation."
    )

    if question_type == "mcq" and correct_answer:
        # Simple exact match for MCQ
        is_correct = _normalize(student_answer) == _normalize(correct_answer)
        score = 1.0 if is_correct else 0.0
        confidence = 0.95 if is_correct else 0.85
        misconception = None if is_correct else f"Incorrect understanding of {concept}"
        next_action = "continue" if is_correct else "re_explain_with_analogy"

    elif question_type in ("short_answer", "conceptual", "explain"):
        # For open-ended questions, check if the answer contains the concept
        answer_lower = student_answer.lower()
        concept_lower = concept.lower()

        if concept_lower and concept_lower in answer_lower:
            is_correct = True
            score = 0.8
            confidence = 0.7
            misconception = None
            next_action = "continue"
        elif len(student_answer.strip()) < 5:
            is_correct = False
            score = 0.1
            confidence = 0.9
            misconception = "Answer too brief to assess understanding"
            next_action = "re_explain"
        else:
            is_correct = False
            score = 0.4
            confidence = 0.5
            misconception = f"Partial understanding of {concept}"
            next_action = "re_explain_with_analogy"
    else:
        is_correct = False
        score = 0.0
        confidence = 0.5
        misconception = None
        next_action = "re_explain"

    return StudentEvaluation(
        question_id=question_id,
        correct=is_correct,
        score=score,
        concept=concept,
        misconception=misconception,
        confidence=confidence,
        next_action=next_action,
        difficulty=difficulty,
    )


def _normalize(text: str) -> str:
    """Normalize text for comparison."""
    return text.strip().lower()
