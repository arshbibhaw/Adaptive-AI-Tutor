"""
Assessment model.

Stores final assessment results for a session.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    session_id: Mapped[str] = mapped_column(
        String, ForeignKey("sessions.id"), nullable=False
    )
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    strong_concepts: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    weak_concepts: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    misconceptions: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    revision_recommendations: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    next_topic: Mapped[str | None] = mapped_column(String, nullable=True)
    report: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    session = relationship("Session", back_populates="assessments")
