"""
Adaptation service.

Implements the MVP adaptation rules for adjusting lesson difficulty
and teaching strategy based on student performance.

Rules per Team 3 spec:
  2 correct → increase difficulty
  1 incorrect → re-explain
  2 incorrect on same concept → simplify
  3 failures → mark weak + recommend revision
"""

import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class AdaptationEngine:
    """
    Tracks student performance per concept and decides adaptation actions.
    """

    def __init__(self):
        # Track per-concept performance: {concept: {"correct": int, "incorrect": int}}
        self._performance: dict[str, dict] = defaultdict(
            lambda: {"correct": 0, "incorrect": 0, "consecutive_incorrect": 0}
        )
        self._current_difficulty: str = "medium"

    def record_result(self, concept: str, correct: bool) -> None:
        """Record a question result for a concept."""
        perf = self._performance[concept]
        if correct:
            perf["correct"] += 1
            perf["consecutive_incorrect"] = 0
        else:
            perf["incorrect"] += 1
            perf["consecutive_incorrect"] += 1

    def decide_action(self, concept: str) -> dict:
        """
        Decide the next adaptation action based on performance history.

        Returns:
            {
                "action": str,
                "difficulty": str,
                "reason": str,
            }
        """
        perf = self._performance[concept]
        correct = perf["correct"]
        consecutive_incorrect = perf["consecutive_incorrect"]
        total_incorrect = perf["incorrect"]

        # Rule: 3+ failures → mark weak + recommend revision
        if total_incorrect >= 3:
            logger.info("Concept '%s': 3+ failures → marking weak.", concept)
            return {
                "action": "mark_weak",
                "difficulty": self._current_difficulty,
                "reason": f"3+ incorrect answers on {concept}. Recommending revision.",
            }

        # Rule: 2 incorrect on same concept → simplify
        if consecutive_incorrect >= 2:
            self._current_difficulty = "easy"
            logger.info("Concept '%s': 2 consecutive incorrect → simplifying.", concept)
            return {
                "action": "simplify",
                "difficulty": "easy",
                "reason": f"2 consecutive incorrect answers on {concept}. Simplifying.",
            }

        # Rule: 1 incorrect → re-explain
        if consecutive_incorrect >= 1:
            logger.info("Concept '%s': 1 incorrect → re-explaining.", concept)
            return {
                "action": "re_explain",
                "difficulty": self._current_difficulty,
                "reason": f"Incorrect answer on {concept}. Re-explaining.",
            }

        # Rule: 2+ correct → increase difficulty
        if correct >= 2:
            self._current_difficulty = _increase_difficulty(self._current_difficulty)
            logger.info("Concept '%s': 2+ correct → increasing difficulty.", concept)
            return {
                "action": "increase_difficulty",
                "difficulty": self._current_difficulty,
                "reason": f"2+ correct answers on {concept}. Increasing difficulty.",
            }

        # Default: continue
        return {
            "action": "continue",
            "difficulty": self._current_difficulty,
            "reason": "Continuing with current approach.",
        }

    def get_performance_summary(self) -> dict:
        """Return a summary of all concept performance."""
        return dict(self._performance)


def _increase_difficulty(current: str) -> str:
    """Increase difficulty by one step."""
    levels = ["easy", "medium", "hard"]
    idx = levels.index(current) if current in levels else 1
    return levels[min(idx + 1, len(levels) - 1)]
