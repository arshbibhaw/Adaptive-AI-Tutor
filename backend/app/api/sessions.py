"""
Sessions API endpoints.

POST /sessions — Create a new teaching session.
POST /sessions/{id}/start — Start a teaching session (generate lesson plan).
POST /sessions/{id}/answer — Submit a student answer.
GET  /sessions/{id}/progress — Get session progress.
GET  /sessions/{id}/report — Get the learning report.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user_id
from backend.app.models.session import Session
from backend.app.models.document import Document
from backend.app.models.assessment import Assessment as AssessmentModel
from backend.app.schemas.lesson import SessionCreate, SessionResponse, SessionStartResponse
from backend.app.schemas.evaluation import AnswerSubmission, AnswerResponse
from backend.app.schemas.progress import LearningReportResponse
from backend.app.services.teacher.planner import generate_lesson_plan
from backend.app.services.teacher.teacher_agent import TeacherAgent
from backend.app.services.teacher.lesson_state import LessonState
from backend.app.services.assessment.evaluator import evaluate_answer
from backend.app.services.assessment.misconception import detect_misconception
from backend.app.services.assessment.adaptation import AdaptationEngine
from backend.app.services.assessment.question_generator import generate_question
from backend.app.services.assessment.report import generate_learning_report
from backend.app.services.learner.history import record_interaction
from backend.app.services.learner.progress import record_progress
from backend.app.services.rag.retriever import retrieve

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=SessionResponse)
async def create_session(
    data: SessionCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new teaching session."""
    if not data.topic and not data.document_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'topic' or 'document_id' must be provided.",
        )

    # Validate document if provided
    if data.document_id:
        result = await db.execute(
            select(Document).where(Document.id == data.document_id, Document.user_id == user_id)
        )
        doc = result.scalar_one_or_none()
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    session = Session(
        user_id=user_id,
        topic=data.topic,
        document_id=data.document_id,
        language=data.language,
        learner_level=data.learner_level,
        duration_minutes=data.duration_minutes,
        goal=data.goal,
        status="created",
    )
    db.add(session)
    await db.flush()
    await db.refresh(session)

    logger.info("Session created: %s (topic=%s, doc=%s)", session.id, data.topic, data.document_id)

    return SessionResponse(
        id=session.id,
        topic=session.topic,
        document_id=session.document_id,
        language=session.language,
        learner_level=session.learner_level,
        duration_minutes=session.duration_minutes,
        status=session.status,
        lesson_plan=session.lesson_plan,
        lesson_state=session.lesson_state,
    )


@router.post("/{session_id}/start", response_model=SessionStartResponse)
async def start_session(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Start a session: generate lesson plan and begin teaching."""
    result = await db.execute(
        select(Session).where(Session.id == session_id, Session.user_id == user_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    # Get document outline if document-based
    doc_outline = None
    retrieved_context = None
    if session.document_id:
        doc_result = await db.execute(
            select(Document).where(Document.id == session.document_id)
        )
        doc = doc_result.scalar_one_or_none()
        if doc:
            doc_outline = doc.outline
            # Retrieve context for the topic
            if session.topic and doc.status == "indexed":
                retrieved_context = await retrieve(session.topic, session.document_id)

    # Generate lesson plan
    session.status = "planning"
    await db.flush()

    lesson_plan = await generate_lesson_plan(
        topic=session.topic,
        document_outline=doc_outline,
        retrieved_context=retrieved_context,
        learner_level=session.learner_level,
        language=session.language,
        duration_minutes=session.duration_minutes,
        goal=session.goal,
    )

    # Update session
    session.lesson_plan = lesson_plan.model_dump()
    session.lesson_state = LessonState(
        time_remaining=session.duration_minutes,
        current_concept=lesson_plan.segments[0].concept if lesson_plan.segments else "",
    ).to_dict()
    session.status = "teaching"
    await db.flush()

    first_segment = lesson_plan.segments[0] if lesson_plan.segments else None

    logger.info("Session started: %s — %d segments", session_id, len(lesson_plan.segments))

    return SessionStartResponse(
        session_id=session_id,
        lesson_plan=lesson_plan,
        first_segment=first_segment,
        message=f"Lesson plan ready: {lesson_plan.title} ({len(lesson_plan.segments)} segments).",
    )


@router.post("/{session_id}/answer", response_model=AnswerResponse)
async def submit_answer(
    session_id: str,
    data: AnswerSubmission,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Submit a student answer and get evaluation + adaptation."""
    result = await db.execute(
        select(Session).where(Session.id == session_id, Session.user_id == user_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    # Determine concept from session state
    lesson_state = LessonState.from_dict(session.lesson_state or {})
    concept = data.concept or lesson_state.current_concept

    # Evaluate answer
    evaluation = await evaluate_answer(
        question_id=data.question_id,
        student_answer=data.answer,
        concept=concept,
    )

    # Detect misconception if incorrect
    misconception_data = None
    if not evaluation.correct:
        misconception_data = await detect_misconception(
            concept=concept,
            student_answer=data.answer,
        )
        if misconception_data.get("misconception"):
            evaluation.misconception = misconception_data["misconception"]

    # Record interaction in DB
    await record_interaction(
        db=db,
        session_id=session_id,
        interaction_type="answer",
        concept=concept,
        question_text=None,
        student_answer=data.answer,
        correct=evaluation.correct,
        score=evaluation.score,
        misconception=evaluation.misconception,
        confidence=evaluation.confidence,
        next_action=evaluation.next_action,
    )

    # Run adaptation engine
    adaptation_engine = AdaptationEngine()
    adaptation_engine.record_result(concept, evaluation.correct)
    adaptation = adaptation_engine.decide_action(concept)

    # Update lesson state
    if evaluation.correct:
        lesson_state.record_correct()
    else:
        lesson_state.record_incorrect()
    session.lesson_state = lesson_state.to_dict()
    await db.flush()

    # Generate next question if continuing
    next_question_data = None
    if evaluation.correct or adaptation["action"] in ("continue", "increase_difficulty"):
        next_q = await generate_question(
            concept=concept,
            learner_level=session.learner_level,
            language=session.language,
            difficulty=adaptation.get("difficulty", "medium"),
        )
        next_question_data = next_q.model_dump()

    # Build feedback message
    if evaluation.correct:
        feedback = "Correct! Well done."
    elif evaluation.misconception:
        feedback = f"Not quite. {evaluation.misconception}. Let me explain differently."
    else:
        feedback = "That's not right. Let me help you understand this better."

    logger.info(
        "Answer evaluated for session %s: correct=%s, action=%s",
        session_id, evaluation.correct, adaptation["action"],
    )

    return AnswerResponse(
        evaluation=evaluation,
        feedback=feedback,
        next_question=next_question_data,
        adaptation=adaptation,
    )


@router.get("/{session_id}/progress")
async def get_progress(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get the current progress for a session."""
    result = await db.execute(
        select(Session).where(Session.id == session_id, Session.user_id == user_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    lesson_state = LessonState.from_dict(session.lesson_state or {})

    return {
        "session_id": session_id,
        "status": session.status,
        "lesson_state": lesson_state.to_dict(),
        "lesson_plan": session.lesson_plan,
    }


@router.get("/{session_id}/report", response_model=LearningReportResponse)
async def get_report(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get the final learning report for a session."""
    result = await db.execute(
        select(Session).where(Session.id == session_id, Session.user_id == user_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    lesson_state = LessonState.from_dict(session.lesson_state or {})
    lesson_plan = session.lesson_plan or {}

    # Generate report
    report = await generate_learning_report(
        session_id=session_id,
        concepts_covered=lesson_state.completed_concepts,
        strong_concepts=lesson_state.strong_concepts,
        weak_concepts=lesson_state.weak_concepts,
        misconceptions=[],  # TODO: aggregate from interactions
        total_questions=lesson_state.total_questions_asked,
        correct_answers=lesson_state.total_correct,
        topic=session.topic or lesson_plan.get("title", ""),
    )

    # Record progress to DB
    for concept in lesson_state.strong_concepts:
        await record_progress(
            db=db, user_id=user_id, session_id=session_id,
            topic=session.topic or "", concept=concept,
            mastery=0.9, attempts=1, correct_count=1,
        )
    for concept in lesson_state.weak_concepts:
        await record_progress(
            db=db, user_id=user_id, session_id=session_id,
            topic=session.topic or "", concept=concept,
            mastery=0.3, attempts=1, correct_count=0,
            misconceptions=[],
        )

    # Update session status
    session.status = "completed"
    await db.flush()

    return report
