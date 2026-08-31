"""
Learner profile model.

Stores learner preferences, level, language, goals, and concept mastery.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id"), unique=True, nullable=False
    )
    level: Mapped[str] = mapped_column(String, default="beginner")  # beginner | intermediate | advanced
    language: Mapped[str] = mapped_column(String, default="en")
    goals: Mapped[str | None] = mapped_column(String, nullable=True)
    preferences: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    strong_concepts: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    weak_concepts: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    learning_history: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="learner_profile")
