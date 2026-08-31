"""
Learner history service.

Session history and interaction logs.
"""

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.session import Session
from backend.app.models.interaction import Interaction

logger = logging.getLogger(__name__)


async def get_session_history(
    db: AsyncSession,
    user_id: str,
    limit: int = 20,
) -> list[dict]:
    """Get recent session history for a user."""
    result = await db.execute(
        select(Session)
        .where(Session.user_id == user_id)
        .order_by(Session.created_at.desc())
        .limit(limit)
    )
    sessions = result.scalars().all()

    return [
        {
            "id": s.id,
            "topic": s.topic,
            "language": s.language,
            "learner_level": s.learner_level,
            "duration_minutes": s.duration_minutes,
            "status": s.status,
            "created_at": s.created_at.isoformat() if s.created_at else None,
        }
        for s in sessions
    ]


async def get_session_interactions(
    db: AsyncSession,
    session_id: str,
) -> list[dict]:
    """Get all interactions for a session."""
    result = await db.execute(
        select(Interaction)
        .where(Interaction.session_id == session_id)
        .order_by(Interaction.created_at.asc())
    )
    interactions = result.scalars().all()

    return [
        {
            "id": i.id,
            "interaction_type": i.interaction_type,
            "concept": i.concept,
            "question_text": i.question_text,
            "student_answer": i.student_answer,
            "correct": i.correct,
            "score": i.score,
            "misconception": i.misconception,
            "next_action": i.next_action,
            "created_at": i.created_at.isoformat() if i.created_at else None,
        }
        for i in interactions
    ]


async def record_interaction(
    db: AsyncSession,
    session_id: str,
    interaction_type: str,
    concept: str | None = None,
    question_text: str | None = None,
    question_type: str | None = None,
    student_answer: str | None = None,
    correct: bool | None = None,
    score: float | None = None,
    misconception: str | None = None,
    confidence: float | None = None,
    next_action: str | None = None,
    metadata: dict | None = None,
) -> Interaction:
    """Record a teaching interaction."""
    interaction = Interaction(
        session_id=session_id,
        interaction_type=interaction_type,
        concept=concept,
        question_text=question_text,
        question_type=question_type,
        student_answer=student_answer,
        correct=correct,
        score=score,
        misconception=misconception,
        confidence=confidence,
        next_action=next_action,
        metadata=metadata,
    )
    db.add(interaction)
    await db.flush()
    logger.info("Recorded interaction for session %s: %s", session_id, interaction_type)
    return interaction
