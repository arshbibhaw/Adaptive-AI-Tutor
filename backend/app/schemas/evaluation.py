"""
Evaluation schemas.

Pydantic models for the StudentEvaluation shared contract.
"""

from pydantic import BaseModel


class StudentEvaluation(BaseModel):
    """
    Shared StudentEvaluation contract.

    Used by: Assessment (Team 3), Teacher Agent (Team 2), Frontend (Team 5).
    """
    question_id: str
    correct: bool
    score: float = 0.0
    concept: str = ""
    misconception: str | None = None
    confidence: float = 0.0
    next_action: str = ""  # continue | re_explain | simplify | analogy | worked_example | visual | re_test | mark_weak
    difficulty: str = "medium"  # easy | medium | hard


class AnswerSubmission(BaseModel):
    """Request to submit a student answer."""
    question_id: str
    answer: str
    concept: str | None = None


class AnswerResponse(BaseModel):
    """Response after evaluating a student answer."""
    evaluation: StudentEvaluation
    feedback: str
    next_question: dict | None = None
    adaptation: dict | None = None


class QuestionGenerated(BaseModel):
    """A generated question for the student."""
    id: str
    question_text: str
    question_type: str  # mcq | short_answer | conceptual | numerical | explain
    concept: str
    difficulty: str = "medium"
    options: list[str] | None = None  # For MCQ
    correct_answer: str | None = None
    language: str = "en"
