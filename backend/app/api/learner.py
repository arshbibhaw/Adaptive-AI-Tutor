"""
Learner API endpoints.

POST /learner/register — Register a new user.
POST /learner/login — Log in.
GET  /learner/profile — Get learner profile.
PUT  /learner/profile — Update learner profile.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user_id
from backend.app.core.security import hash_password, verify_password, create_access_token
from backend.app.models.user import User
from backend.app.schemas.learner import (
    UserRegister,
    UserLogin,
    TokenResponse,
    LearnerProfileCreate,
    LearnerProfileResponse,
)
from backend.app.services.learner.profile import get_profile, create_or_update_profile

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(
    data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user."""
    # Check if email exists
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    token = create_access_token({"sub": user.id})
    logger.info("User registered: %s (id=%s)", data.email, user.id)

    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """Log in with email and password."""
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = create_access_token({"sub": user.id})
    logger.info("User logged in: %s", data.email)

    return TokenResponse(access_token=token)


@router.get("/profile", response_model=LearnerProfileResponse | None)
async def get_learner_profile(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get the learner profile for the current user."""
    profile = await get_profile(db, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner profile not found. Create one first.",
        )
    return profile


@router.put("/profile", response_model=LearnerProfileResponse)
async def update_learner_profile(
    data: LearnerProfileCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create or update the learner profile."""
    return await create_or_update_profile(db, user_id, data)
