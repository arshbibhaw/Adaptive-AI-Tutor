"""
Progress model.

Tracks per-concept learning progress across sessions.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class Progress(Base):
    __tablename__ = "progress"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    session_id: Mapped[str] = mapped_column(
        String, ForeignKey("sessions.id"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id"), nullable=False
    )
    topic: Mapped[str] = mapped_column(String, nullable=False)
    concept: Mapped[str | None] = mapped_column(String, nullable=True)
    mastery: Mapped[float] = mapped_column(Float, default=0.0)  # 0.0 to 1.0
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    misconceptions: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    status: Mapped[str] = mapped_column(String, default="in_progress")  # in_progress | mastered | weak | needs_revision
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    session = relationship("Session", back_populates="progress")
