"""
Teacher agent service.

The core orchestration brain implementing the teaching state machine:
Introduction → Explanation → Demonstration → Question → Evaluation →
Adaptation → Continue → FinalAssessment → Completed.

============================================================
PLACEHOLDER — LLM provider not yet configured.
============================================================
TODO: When the LLM provider is selected, replace placeholder
explanation/teaching generation with actual LLM calls that:
  - Generate contextual explanations grounded in RAG context
  - Produce teaching scripts for video generation
  - Generate follow-up based on student evaluation
  - Adapt explanations using alternative strategies
============================================================
"""

import logging

from backend.app.schemas.lesson import LessonPlan, LessonSegment
from backend.app.schemas.evaluation import StudentEvaluation
from backend.app.services.teacher.lesson_state import LessonState
from backend.app.services.teacher.planner import generate_lesson_plan
from backend.app.services.teacher.personalization import get_personalization_context

logger = logging.getLogger(__name__)


class TeacherAgent:
    """
    The AI Teacher orchestration engine.

    Manages the teaching lifecycle for a session, coordinating
    between RAG retrieval, lesson planning, assessment, and video generation.
    """

    def __init__(
        self,
        lesson_plan: LessonPlan,
        lesson_state: LessonState | None = None,
        retrieved_context: list[dict] | None = None,
    ):
        self.lesson_plan = lesson_plan
        self.state = lesson_state or LessonState(
            time_remaining=lesson_plan.duration_minutes,
            current_concept=lesson_plan.segments[0].concept if lesson_plan.segments else "",
        )
        self.retrieved_context = retrieved_context or []

    def get_current_segment(self) -> LessonSegment | None:
        """Get the current lesson segment."""
        idx = self.state.current_segment_index
        if idx < len(self.lesson_plan.segments):
            return self.lesson_plan.segments[idx]
        return None

    async def start_lesson(self) -> dict:
        """
        Start the lesson — produce the introduction.

        ============================================================
        PLACEHOLDER: Returns static introduction text.
        Replace with LLM-generated introduction when configured.
        ============================================================
        """
        self.state.phase = "introduction"
        segment = self.get_current_segment()
        concept = segment.concept if segment else self.lesson_plan.title

        logger.info("Starting lesson: %s", self.lesson_plan.title)

        return {
            "phase": "introduction",
            "message": (
                f"Welcome! Today we'll learn about {self.lesson_plan.title}. "
                f"This lesson is designed for {self.lesson_plan.learner_level} level "
                f"and will take about {self.lesson_plan.duration_minutes} minutes. "
                f"Let's start with {concept}."
            ),
            "segment": segment.model_dump() if segment else None,
            "lesson_state": self.state.to_dict(),
        }

    async def explain_current(self) -> dict:
        """
        Explain the current concept.

        ============================================================
        PLACEHOLDER: Returns static explanation.
        Replace with LLM-generated explanation grounded in RAG context.
        ============================================================
        """
        self.state.phase = "explanation"
        segment = self.get_current_segment()

        if not segment:
            return await self.complete_lesson()

        logger.info("Explaining concept: %s", segment.concept)

        # Build context summary from retrieved chunks
        context_summary = ""
        if self.retrieved_context:
            context_texts = [c.get("text", "") for c in self.retrieved_context[:3]]
            context_summary = " Based on the source material: " + " ".join(context_texts)[:500]

        return {
            "phase": "explanation",
            "concept": segment.concept,
            "explanation": (
                f"Let me explain {segment.concept}. "
                f"{segment.explanation}"
                f"{context_summary}"
            ),
            "example": segment.example,
            "visual_type": segment.visual_type,
            "segment": segment.model_dump(),
            "lesson_state": self.state.to_dict(),
        }

    async def handle_evaluation(self, evaluation: StudentEvaluation) -> dict:
        """
        Process a student evaluation and decide the next action.

        Implements the decision rules from Team 2 spec:
        - Correct → continue or increase difficulty
        - Incorrect → re-explain
        - Repeated incorrect → simplify and retry
        - Time low → prioritize high-value concepts
        """
        self.state.last_evaluation = evaluation.model_dump()

        if evaluation.correct:
            self.state.record_correct()
            concept = evaluation.concept or self.state.current_concept
            self.state.mark_concept_strong(concept)

            # Decide: continue to next segment or increase difficulty
            if self.state.consecutive_incorrect == 0:
                return await self._advance_to_next()
        else:
            self.state.record_incorrect()

            if evaluation.misconception:
                logger.info(
                    "Misconception detected for concept '%s': %s",
                    evaluation.concept,
                    evaluation.misconception,
                )

            # Decide adaptation strategy based on consecutive failures
            if self.state.consecutive_incorrect >= 3:
                # 3+ failures → mark weak and move on
                concept = evaluation.concept or self.state.current_concept
                self.state.mark_concept_weak(concept)
                return await self._mark_weak_and_continue(concept, evaluation)
            elif self.state.consecutive_incorrect >= 2:
                # 2 failures → simplify
                return await self._simplify_and_reteach(evaluation)
            else:
                # 1 failure → re-explain with different approach
                return await self._reteach(evaluation)

        return await self._advance_to_next()

    async def generate_final_assessment(self) -> dict:
        """
        Transition to the final assessment phase.

        ============================================================
        PLACEHOLDER: Returns static assessment info.
        Replace with LLM-generated final quiz when configured.
        ============================================================
        """
        self.state.phase = "final_assessment"
        logger.info("Starting final assessment for: %s", self.lesson_plan.title)

        return {
            "phase": "final_assessment",
            "message": "Great work! Let's test your understanding with a final assessment.",
            "concepts_covered": self.state.completed_concepts,
            "lesson_state": self.state.to_dict(),
        }

    async def complete_lesson(self) -> dict:
        """Complete the lesson and generate summary."""
        self.state.phase = "completed"
        logger.info("Lesson completed: %s", self.lesson_plan.title)

        accuracy = (
            self.state.total_correct / self.state.total_questions_asked
            if self.state.total_questions_asked > 0
            else 0.0
        )

        return {
            "phase": "completed",
            "message": "Congratulations! You've completed this lesson.",
            "summary": {
                "total_questions": self.state.total_questions_asked,
                "correct_answers": self.state.total_correct,
                "accuracy": round(accuracy, 2),
                "strong_concepts": self.state.strong_concepts,
                "weak_concepts": self.state.weak_concepts,
                "completed_concepts": self.state.completed_concepts,
            },
            "lesson_state": self.state.to_dict(),
        }

    # --- Private helpers ---

    async def _advance_to_next(self) -> dict:
        """Advance to the next segment or final assessment."""
        segment = self.get_current_segment()
        if segment:
            self.state.mark_concept_completed(segment.concept)

        self.state.advance_segment()
        next_segment = self.get_current_segment()

        if next_segment is None:
            # No more segments — go to final assessment
            return await self.generate_final_assessment()

        self.state.current_concept = next_segment.concept
        self.state.phase = "explanation"

        logger.info("Advancing to next concept: %s", next_segment.concept)

        return {
            "phase": "continue",
            "message": f"Great! Let's move on to {next_segment.concept}.",
            "segment": next_segment.model_dump(),
            "lesson_state": self.state.to_dict(),
        }

    async def _reteach(self, evaluation: StudentEvaluation) -> dict:
        """
        Re-explain the current concept with a different approach.

        ============================================================
        PLACEHOLDER: Returns static re-explanation.
        Replace with LLM-generated alternative explanation.
        ============================================================
        """
        self.state.phase = "adaptation"
        concept = evaluation.concept or self.state.current_concept
        logger.info("Re-teaching concept: %s (approach: alternative explanation)", concept)

        return {
            "phase": "adaptation",
            "action": "re_explain",
            "concept": concept,
            "misconception": evaluation.misconception,
            "message": (
                f"Let me try explaining {concept} differently. "
                f"{'I noticed you might be thinking: ' + evaluation.misconception + '. ' if evaluation.misconception else ''}"
                f"Let's look at it from another angle."
            ),
            "lesson_state": self.state.to_dict(),
        }

    async def _simplify_and_reteach(self, evaluation: StudentEvaluation) -> dict:
        """
        Simplify and re-teach with a basic analogy.

        ============================================================
        PLACEHOLDER: Returns static simplified explanation.
        Replace with LLM-generated simplified explanation.
        ============================================================
        """
        self.state.phase = "adaptation"
        concept = evaluation.concept or self.state.current_concept
        logger.info("Simplifying concept: %s (consecutive failures: %d)", concept, self.state.consecutive_incorrect)

        return {
            "phase": "adaptation",
            "action": "simplify",
            "concept": concept,
            "misconception": evaluation.misconception,
            "message": (
                f"Let me simplify {concept} with a basic analogy. "
                f"Think of it this way..."
            ),
            "lesson_state": self.state.to_dict(),
        }

    async def _mark_weak_and_continue(self, concept: str, evaluation: StudentEvaluation) -> dict:
        """Mark concept as weak and recommend revision, then continue."""
        self.state.phase = "adaptation"
        logger.info("Marking concept as weak: %s (moving on)", concept)

        return {
            "phase": "adaptation",
            "action": "mark_weak",
            "concept": concept,
            "message": (
                f"It seems {concept} needs more practice. I've noted it for revision. "
                f"Let's continue with the next topic for now."
            ),
            "revision_recommended": True,
            "lesson_state": self.state.to_dict(),
        }
