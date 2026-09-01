"""
Interaction model.

Stores individual teaching interactions within a session (questions, answers, adaptations).
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    session_id: Mapped[str] = mapped_column(
        String, ForeignKey("sessions.id"), nullable=False
    )
    interaction_type: Mapped[str] = mapped_column(String, nullable=False)  # question | answer | explanation | adaptation
    concept: Mapped[str | None] = mapped_column(String, nullable=True)
    question_text: Mapped[str | None] = mapped_column(String, nullable=True)
    question_type: Mapped[str | None] = mapped_column(String, nullable=True)  # mcq | short_answer | conceptual | numerical
    student_answer: Mapped[str | None] = mapped_column(String, nullable=True)
    correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    misconception: Mapped[str | None] = mapped_column(String, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    next_action: Mapped[str | None] = mapped_column(String, nullable=True)
    extra_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    session = relationship("Session", back_populates="interactions")
