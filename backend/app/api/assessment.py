"""
Assessment API endpoints.

POST /assessment/{session_id}/quiz — Generate final assessment quiz.
POST /assessment/{session_id}/submit — Submit final assessment answers.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user_id
from backend.app.models.session import Session
from backend.app.models.assessment import Assessment as AssessmentModel
from backend.app.services.teacher.lesson_state import LessonState
from backend.app.services.assessment.question_generator import generate_final_quiz
from backend.app.services.assessment.evaluator import evaluate_answer

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/{session_id}/quiz")
async def generate_quiz(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Generate a final assessment quiz for a session."""
    result = await db.execute(
        select(Session).where(Session.id == session_id, Session.user_id == user_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    lesson_state = LessonState.from_dict(session.lesson_state or {})
    concepts = lesson_state.completed_concepts or ["General"]

    questions = await generate_final_quiz(
        concepts=concepts,
        learner_level=session.learner_level,
        language=session.language,
    )

    session.status = "assessing"
    await db.flush()

    return {
        "session_id": session_id,
        "questions": [q.model_dump() for q in questions],
        "total_questions": len(questions),
    }


@router.post("/{session_id}/submit")
async def submit_quiz(
    session_id: str,
    answers: list[dict],
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Submit final assessment answers and get results."""
    result = await db.execute(
        select(Session).where(Session.id == session_id, Session.user_id == user_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    evaluations = []
    correct_count = 0

    for answer_data in answers:
        evaluation = await evaluate_answer(
            question_id=answer_data.get("question_id", ""),
            student_answer=answer_data.get("answer", ""),
            correct_answer=answer_data.get("correct_answer"),
            concept=answer_data.get("concept", ""),
            question_type=answer_data.get("question_type", "mcq"),
        )
        evaluations.append(evaluation.model_dump())
        if evaluation.correct:
            correct_count += 1

    total = len(answers)
    score = correct_count / total if total > 0 else 0.0

    # Store assessment
    lesson_state = LessonState.from_dict(session.lesson_state or {})
    assessment = AssessmentModel(
        session_id=session_id,
        total_questions=total,
        correct_answers=correct_count,
        score=round(score, 2),
        strong_concepts=lesson_state.strong_concepts,
        weak_concepts=lesson_state.weak_concepts,
    )
    db.add(assessment)
    await db.flush()

    logger.info("Quiz submitted for session %s: %d/%d correct (%.0f%%)", session_id, correct_count, total, score * 100)

    return {
        "session_id": session_id,
        "total_questions": total,
        "correct_answers": correct_count,
        "score": round(score, 2),
        "evaluations": evaluations,
    }
