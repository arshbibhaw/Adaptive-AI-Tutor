import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.app.core.database import Base
from backend.app.models.user import User
from backend.app.models.learner import LearnerProfile
from backend.app.models.document import Document
from backend.app.models.session import Session
from backend.app.models.lesson_plan import LessonPlan
from backend.app.models.interaction import Interaction
from backend.app.models.assessment import Assessment
from backend.app.models.progress import Progress
from backend.app.models.learning_report import LearningReport


@pytest_asyncio.fixture
async def test_db_session():
    """Create an in-memory SQLite database for testing models and relations."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_user_and_learner_profile(test_db_session: AsyncSession):
    """Test User and LearnerProfile creation and relationship."""
    user = User(
        email="student@example.com",
        hashed_password="hashed_secret_pw",
        full_name="Alex Student",
    )
    test_db_session.add(user)
    await test_db_session.flush()

    profile = LearnerProfile(
        user_id=user.id,
        level="intermediate",
        language="hi",
        goals="Pass Physics exam",
        preferences={"avatar": "friendly", "voice_speed": 1.1},
        strong_concepts=["Ohm's Law", "Voltage"],
        weak_concepts=["Resistance Calculation"],
        learning_history=[{"topic": "Circuits", "date": "2026-09-01"}],
    )
    test_db_session.add(profile)
    await test_db_session.commit()

    # Query back with eager loading
    result = await test_db_session.execute(
        select(User)
        .options(selectinload(User.learner_profile))
        .where(User.email == "student@example.com")
    )
    queried_user = result.scalar_one()

    assert queried_user is not None
    assert queried_user.full_name == "Alex Student"
    assert queried_user.learner_profile.level == "intermediate"
    assert queried_user.learner_profile.language == "hi"
    assert queried_user.learner_profile.goals == "Pass Physics exam"
    assert "Voltage" in queried_user.learner_profile.strong_concepts


@pytest.mark.asyncio
async def test_full_session_hierarchy(test_db_session: AsyncSession):
    """Test full hierarchy: User -> Document, Session -> LessonPlan, Interaction, Assessment, Progress, LearningReport."""
    # 1. User
    user = User(email="tutor_user@example.com", hashed_password="pw")
    test_db_session.add(user)
    await test_db_session.flush()

    # 2. Document
    doc = Document(
        user_id=user.id,
        filename="photosynthesis.pdf",
        file_type="pdf",
        file_size=10240,
        file_path="/data/uploads/photosynthesis.pdf",
        status="indexed",
        chunk_count=5,
        outline={"title": "Photosynthesis", "sections": [{"heading": "Light Reactions"}]},
    )
    test_db_session.add(doc)
    await test_db_session.flush()

    # 3. Session
    session = Session(
        user_id=user.id,
        document_id=doc.id,
        topic="Photosynthesis",
        language="en",
        learner_level="beginner",
        duration_minutes=20,
        status="teaching",
    )
    test_db_session.add(session)
    await test_db_session.flush()

    # 4. LessonPlan
    lesson_plan = LessonPlan(
        session_id=session.id,
        title="Introduction to Photosynthesis",
        duration_minutes=20,
        language="en",
        learner_level="beginner",
        segments=[
            {"id": "seg1", "concept": "Chloroplasts", "minutes": 5, "checkpoint": True}
        ],
    )
    test_db_session.add(lesson_plan)

    # 5. Interaction
    interaction = Interaction(
        session_id=session.id,
        interaction_type="question",
        concept="Chloroplasts",
        question_text="Where does photosynthesis take place?",
        question_type="mcq",
        student_answer="Chloroplasts",
        correct=True,
        score=1.0,
        confidence=0.95,
        next_action="continue",
    )
    test_db_session.add(interaction)

    # 6. Assessment
    assessment = Assessment(
        session_id=session.id,
        total_questions=5,
        correct_answers=4,
        score=0.8,
        strong_concepts=["Chloroplasts"],
        weak_concepts=["Calvin Cycle"],
        next_topic="Cellular Respiration",
    )
    test_db_session.add(assessment)

    # 7. Progress
    progress = Progress(
        session_id=session.id,
        user_id=user.id,
        topic="Photosynthesis",
        concept="Chloroplasts",
        mastery=0.9,
        attempts=1,
        correct_count=1,
        status="mastered",
    )
    test_db_session.add(progress)

    # 8. LearningReport
    report = LearningReport(
        session_id=session.id,
        user_id=user.id,
        total_questions=5,
        correct_answers=4,
        score=0.8,
        strong_concepts=["Chloroplasts"],
        weak_concepts=["Calvin Cycle"],
        revision_recommendations=["Review dark reactions in Calvin Cycle"],
        next_topic="Cellular Respiration",
        summary="Good understanding of core light reaction concepts.",
    )
    test_db_session.add(report)
    await test_db_session.commit()

    # Verify query and all relationships
    result = await test_db_session.execute(
        select(Session)
        .options(
            selectinload(Session.user),
            selectinload(Session.lesson_plan_record),
            selectinload(Session.interactions),
            selectinload(Session.assessments),
            selectinload(Session.learning_report),
            selectinload(Session.progress),
        )
        .where(Session.id == session.id)
    )
    queried_session = result.scalar_one()

    assert queried_session.user.email == "tutor_user@example.com"
    assert queried_session.lesson_plan_record.title == "Introduction to Photosynthesis"
    assert len(queried_session.interactions) == 1
    assert queried_session.interactions[0].correct is True
    assert len(queried_session.assessments) == 1
    assert queried_session.learning_report.score == 0.8
    assert len(queried_session.progress) == 1
    assert queried_session.progress[0].status == "mastered"
