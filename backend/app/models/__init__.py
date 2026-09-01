"""
Database models package.

Import all models here so SQLAlchemy discovers them for table creation.
"""

from backend.app.models.user import User
from backend.app.models.learner import LearnerProfile
from backend.app.models.document import Document
from backend.app.models.session import Session
from backend.app.models.lesson_plan import LessonPlan
from backend.app.models.interaction import Interaction
from backend.app.models.assessment import Assessment
from backend.app.models.progress import Progress
from backend.app.models.learning_report import LearningReport

__all__ = [
    "User",
    "LearnerProfile",
    "Document",
    "Session",
    "LessonPlan",
    "Interaction",
    "Assessment",
    "Progress",
    "LearningReport",
]
