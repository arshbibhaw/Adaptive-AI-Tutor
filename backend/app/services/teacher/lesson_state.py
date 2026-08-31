"""
Lesson state service.

Tracks the current state of a teaching session through the lesson lifecycle.
"""

import logging
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


@dataclass
class LessonState:
    """
    Tracks where the teacher is within a lesson.

    Used by the Teacher Agent to decide what to do next.
    """
    current_segment_index: int = 0
    current_concept: str = ""
    completed_concepts: list[str] = field(default_factory=list)
    time_remaining: int = 20  # minutes
    weak_concepts: list[str] = field(default_factory=list)
    strong_concepts: list[str] = field(default_factory=list)
    last_evaluation: dict | None = None
    consecutive_incorrect: int = 0
    total_questions_asked: int = 0
    total_correct: int = 0
    phase: str = "introduction"  # introduction | explanation | demonstration | question | evaluation | adaptation | continue | final_assessment | completed

    def to_dict(self) -> dict:
        """Serialize to dict for DB storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LessonState":
        """Deserialize from dict."""
        if not data:
            return cls()
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def mark_concept_completed(self, concept: str) -> None:
        """Mark a concept as completed."""
        if concept and concept not in self.completed_concepts:
            self.completed_concepts.append(concept)

    def mark_concept_weak(self, concept: str) -> None:
        """Mark a concept as weak (needs revision)."""
        if concept and concept not in self.weak_concepts:
            self.weak_concepts.append(concept)

    def mark_concept_strong(self, concept: str) -> None:
        """Mark a concept as strong."""
        if concept and concept not in self.strong_concepts:
            self.strong_concepts.append(concept)

    def advance_segment(self) -> None:
        """Move to the next segment."""
        self.current_segment_index += 1
        self.consecutive_incorrect = 0

    def record_correct(self) -> None:
        """Record a correct answer."""
        self.total_correct += 1
        self.total_questions_asked += 1
        self.consecutive_incorrect = 0

    def record_incorrect(self) -> None:
        """Record an incorrect answer."""
        self.total_questions_asked += 1
        self.consecutive_incorrect += 1
