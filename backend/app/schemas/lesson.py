"""
Lesson schemas.

Pydantic models for the LessonPlan shared contract.
"""

from pydantic import BaseModel


class LessonSegment(BaseModel):
    """A single segment within a lesson plan."""
    id: str
    concept: str
    minutes: int
    explanation: str = ""
    example: str = ""
    visual_type: str = "none"  # diagram | graph | equation | code | timeline | none
    checkpoint: bool = False


class LessonPlan(BaseModel):
    """
    Shared LessonPlan contract.

    Used by: Teacher Agent (Team 2), Frontend (Team 5), Backend (Team 6).
    """
    title: str
    duration_minutes: int = 20
    language: str = "en"
    learner_level: str = "beginner"  # beginner | intermediate | advanced
    segments: list[LessonSegment] = []


class SessionCreate(BaseModel):
    """Request to create a new teaching session."""
    topic: str | None = None
    document_id: str | None = None
    language: str = "en"
    learner_level: str = "beginner"
    duration_minutes: int = 20
    goal: str | None = None


class SessionResponse(BaseModel):
    """Response containing session data."""
    id: str
    topic: str | None
    document_id: str | None
    language: str
    learner_level: str
    duration_minutes: int
    status: str
    lesson_plan: dict | None
    lesson_state: dict | None


class SessionStartResponse(BaseModel):
    """Response when starting a teaching session."""
    session_id: str
    lesson_plan: LessonPlan
    first_segment: LessonSegment | None
    message: str
