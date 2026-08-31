"""
Progress schemas.

Request/response models for learning progress and reports.
"""

from pydantic import BaseModel


class ProgressResponse(BaseModel):
    """Response containing progress for a concept."""
    topic: str
    concept: str | None
    mastery: float
    attempts: int
    correct_count: int
    misconceptions: list | None
    status: str


class LearningReportResponse(BaseModel):
    """Response containing the final learning report for a session."""
    session_id: str
    total_questions: int
    correct_answers: int
    score: float
    strong_concepts: list
    weak_concepts: list
    misconceptions: list
    revision_recommendations: list
    next_topic: str | None


class OverallProgressResponse(BaseModel):
    """Response containing overall learning progress for a user."""
    user_id: str
    topics_studied: list[str]
    total_sessions: int
    average_score: float
    strong_concepts: list
    weak_concepts: list
    current_learning_path: list[str]
