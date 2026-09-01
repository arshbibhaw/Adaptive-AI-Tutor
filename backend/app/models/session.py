"""
Session model.

Stores teaching session metadata linking user, document, lesson plan, and progress.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id"), nullable=False
    )
    document_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("documents.id"), nullable=True
    )
    topic: Mapped[str | None] = mapped_column(String, nullable=True)
    language: Mapped[str] = mapped_column(String, default="en")
    learner_level: Mapped[str] = mapped_column(String, default="beginner")
    duration_minutes: Mapped[int] = mapped_column(Integer, default=20)
    goal: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="created")  # created | planning | teaching | assessing | completed
    lesson_plan: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    lesson_state: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="sessions")
    interactions = relationship("Interaction", back_populates="session", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="session", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="session", cascade="all, delete-orphan")
    lesson_plan_record = relationship("LessonPlan", back_populates="session", uselist=False, cascade="all, delete-orphan")
    learning_report = relationship("LearningReport", back_populates="session", uselist=False, cascade="all, delete-orphan")
