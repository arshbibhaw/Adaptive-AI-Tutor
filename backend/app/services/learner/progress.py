"""
Learner progress service.

Tracks topics studied, scores, mastery, and learning path.
"""

import logging

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.progress import Progress
from backend.app.models.session import Session
from backend.app.models.assessment import Assessment
from backend.app.schemas.progress import ProgressResponse, OverallProgressResponse

logger = logging.getLogger(__name__)


async def record_progress(
    db: AsyncSession,
    user_id: str,
    session_id: str,
    topic: str,
    concept: str,
    mastery: float,
    attempts: int,
    correct_count: int,
    misconceptions: list[str] | None = None,
) -> None:
    """Record or update progress for a concept."""
    # Check for existing progress record
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == user_id,
            Progress.topic == topic,
            Progress.concept == concept,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.mastery = mastery
        existing.attempts += attempts
        existing.correct_count += correct_count
        existing.session_id = session_id
        if misconceptions:
            existing_misc = existing.misconceptions or []
            existing.misconceptions = list(set(existing_misc + misconceptions))
        existing.status = _mastery_status(mastery)
    else:
        progress = Progress(
            user_id=user_id,
            session_id=session_id,
            topic=topic,
            concept=concept,
            mastery=mastery,
            attempts=attempts,
            correct_count=correct_count,
            misconceptions=misconceptions or [],
            status=_mastery_status(mastery),
        )
        db.add(progress)

    await db.flush()
    logger.info("Recorded progress for user %s: %s/%s (mastery: %.2f)", user_id, topic, concept, mastery)


async def get_session_progress(
    db: AsyncSession,
    session_id: str,
) -> list[ProgressResponse]:
    """Get progress entries for a session."""
    result = await db.execute(
        select(Progress).where(Progress.session_id == session_id)
    )
    entries = result.scalars().all()

    return [
        ProgressResponse(
            topic=p.topic,
            concept=p.concept,
            mastery=p.mastery,
            attempts=p.attempts,
            correct_count=p.correct_count,
            misconceptions=p.misconceptions,
            status=p.status,
        )
        for p in entries
    ]


async def get_overall_progress(
    db: AsyncSession,
    user_id: str,
) -> OverallProgressResponse:
    """Get overall learning progress for a user."""
    # Get all progress entries
    result = await db.execute(
        select(Progress).where(Progress.user_id == user_id)
    )
    entries = result.scalars().all()

    # Get total sessions
    session_result = await db.execute(
        select(func.count(Session.id)).where(Session.user_id == user_id)
    )
    total_sessions = session_result.scalar() or 0

    # Aggregate
    topics = list(set(p.topic for p in entries if p.topic))
    strong = [p.concept for p in entries if p.status == "mastered" and p.concept]
    weak = [p.concept for p in entries if p.status in ("weak", "needs_revision") and p.concept]
    scores = [p.mastery for p in entries if p.mastery > 0]
    avg_score = sum(scores) / len(scores) if scores else 0.0

    return OverallProgressResponse(
        user_id=user_id,
        topics_studied=topics,
        total_sessions=total_sessions,
        average_score=round(avg_score, 2),
        strong_concepts=strong,
        weak_concepts=weak,
        current_learning_path=_build_learning_path(topics, weak),
    )


def _mastery_status(mastery: float) -> str:
    """Determine status from mastery score."""
    if mastery >= 0.8:
        return "mastered"
    elif mastery >= 0.5:
        return "in_progress"
    elif mastery > 0:
        return "needs_revision"
    return "weak"


def _build_learning_path(topics: list[str], weak_concepts: list[str]) -> list[str]:
    """Build a simple learning path prioritizing weak concepts."""
    path = []
    for concept in weak_concepts:
        path.append(f"Review: {concept}")
    return path
