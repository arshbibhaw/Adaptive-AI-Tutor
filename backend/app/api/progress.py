"""
Progress API endpoints.

GET /progress — Get overall learning progress for the current user.
"""

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user_id
from backend.app.schemas.progress import OverallProgressResponse
from backend.app.services.learner.progress import get_overall_progress
from backend.app.services.learner.history import get_session_history

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=OverallProgressResponse)
async def get_progress(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get overall learning progress for the current user."""
    return await get_overall_progress(db, user_id)


@router.get("/history")
async def get_history(
    limit: int = 20,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get session history for the current user."""
    return await get_session_history(db, user_id, limit=limit)
