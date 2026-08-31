"""
Question generator service.

Generates questions matching concept, student level, lesson stage, and language.

============================================================
PLACEHOLDER — LLM provider not yet configured.
============================================================
TODO: When the LLM provider is selected, replace static
question generation with LLM-powered generation that produces:
  - MCQs, short answers, conceptual, numerical, explain-in-own-words
  - Questions matching concept, level, stage, and language
============================================================
"""

import logging
import uuid

from backend.app.schemas.evaluation import QuestionGenerated

logger = logging.getLogger(__name__)


async def generate_question(
    concept: str,
    learner_level: str = "beginner",
    question_type: str = "mcq",
    language: str = "en",
    difficulty: str = "medium",
    context: str | None = None,
) -> QuestionGenerated:
    """
    Generate a question for a given concept.

    ============================================================
    PLACEHOLDER: Returns a static question.
    Replace with LLM-generated question when provider is configured.
    ============================================================
    """
    logger.warning(
        "PLACEHOLDER: Using static question. Configure LLM_API_KEY for dynamic generation."
    )

    question_id = str(uuid.uuid4())[:8]

    if question_type == "mcq":
        return QuestionGenerated(
            id=question_id,
            question_text=f"Which of the following best describes {concept}?",
            question_type="mcq",
            concept=concept,
            difficulty=difficulty,
            options=[
                f"Option A: A correct description of {concept}",
                f"Option B: A common misconception about {concept}",
                f"Option C: An unrelated concept",
                f"Option D: A partially correct description",
            ],
            correct_answer=f"Option A: A correct description of {concept}",
            language=language,
        )
    elif question_type == "short_answer":
        return QuestionGenerated(
            id=question_id,
            question_text=f"Explain {concept} in your own words.",
            question_type="short_answer",
            concept=concept,
            difficulty=difficulty,
            options=None,
            correct_answer=None,
            language=language,
        )
    else:
        return QuestionGenerated(
            id=question_id,
            question_text=f"What is {concept}? Explain briefly.",
            question_type="conceptual",
            concept=concept,
            difficulty=difficulty,
            options=None,
            correct_answer=None,
            language=language,
        )


async def generate_final_quiz(
    concepts: list[str],
    learner_level: str = "beginner",
    language: str = "en",
    num_questions: int = 5,
) -> list[QuestionGenerated]:
    """
    Generate a final quiz covering the lesson's concepts.

    ============================================================
    PLACEHOLDER: Returns static questions for each concept.
    Replace with LLM-generated quiz when provider is configured.
    ============================================================
    """
    logger.warning(
        "PLACEHOLDER: Using static final quiz. Configure LLM_API_KEY for dynamic generation."
    )

    questions = []
    for i, concept in enumerate(concepts[:num_questions]):
        q_type = "mcq" if i % 2 == 0 else "short_answer"
        question = await generate_question(
            concept=concept,
            learner_level=learner_level,
            question_type=q_type,
            language=language,
        )
        questions.append(question)

    return questions
