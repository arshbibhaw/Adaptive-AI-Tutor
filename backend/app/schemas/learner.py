"""
Learner schemas.

Request/response models for learner profile operations.
"""

from pydantic import BaseModel


class LearnerProfileCreate(BaseModel):
    """Request to create or update a learner profile."""
    level: str = "beginner"  # beginner | intermediate | advanced
    language: str = "en"
    goals: str | None = None
    preferences: dict | None = None


class LearnerProfileResponse(BaseModel):
    """Response containing learner profile data."""
    id: str
    user_id: str
    level: str
    language: str
    goals: str | None
    preferences: dict | None
    strong_concepts: list | None
    weak_concepts: list | None
    learning_history: list | None


class UserRegister(BaseModel):
    """Request to register a new user."""
    email: str
    password: str
    full_name: str | None = None


class UserLogin(BaseModel):
    """Request to log in."""
    email: str
    password: str


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
