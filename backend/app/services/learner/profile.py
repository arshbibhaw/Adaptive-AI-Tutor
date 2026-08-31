"""
Learner profile service.

CRUD operations for learner profiles: level, language, goals, preferences,
strong/weak concepts.
"""

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.learner import LearnerProfile
from backend.app.schemas.learner import LearnerProfileCreate, LearnerProfileResponse

logger = logging.getLogger(__name__)


async def get_profile(db: AsyncSession, user_id: str) -> LearnerProfileResponse | None:
    """Get the learner profile for a user."""
    result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        return None

    return LearnerProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        level=profile.level,
        language=profile.language,
        goals=profile.goals,
        preferences=profile.preferences,
        strong_concepts=profile.strong_concepts,
        weak_concepts=profile.weak_concepts,
        learning_history=profile.learning_history,
    )


async def create_or_update_profile(
    db: AsyncSession,
    user_id: str,
    data: LearnerProfileCreate,
) -> LearnerProfileResponse:
    """Create or update the learner profile for a user."""
    result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()

    if profile:
        profile.level = data.level
        profile.language = data.language
        profile.goals = data.goals
        profile.preferences = data.preferences
        logger.info("Updated learner profile for user %s.", user_id)
    else:
        profile = LearnerProfile(
            user_id=user_id,
            level=data.level,
            language=data.language,
            goals=data.goals,
            preferences=data.preferences,
        )
        db.add(profile)
        logger.info("Created learner profile for user %s.", user_id)

    await db.flush()
    await db.refresh(profile)

    return LearnerProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        level=profile.level,
        language=profile.language,
        goals=profile.goals,
        preferences=profile.preferences,
        strong_concepts=profile.strong_concepts,
        weak_concepts=profile.weak_concepts,
        learning_history=profile.learning_history,
    )


async def update_concepts(
    db: AsyncSession,
    user_id: str,
    strong: list[str] | None = None,
    weak: list[str] | None = None,
) -> None:
    """Update strong/weak concepts for a learner."""
    result = await db.execute(
        select(LearnerProfile).where(LearnerProfile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        logger.warning("No profile found for user %s to update concepts.", user_id)
        return

    if strong is not None:
        existing = profile.strong_concepts or []
        profile.strong_concepts = list(set(existing + strong))

    if weak is not None:
        existing = profile.weak_concepts or []
        profile.weak_concepts = list(set(existing + weak))

    await db.flush()
    logger.info("Updated concepts for user %s.", user_id)
