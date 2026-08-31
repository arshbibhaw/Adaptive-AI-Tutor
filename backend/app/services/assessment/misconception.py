"""
Misconception detection service.

Identifies likely misconceptions from incorrect answers and
selects remediation strategies.

============================================================
PLACEHOLDER — LLM provider not yet configured.
============================================================
TODO: When the LLM provider is selected, replace static
misconception detection with LLM-powered analysis that:
  - Identifies the specific misconception from the answer
  - Maps it to common misconception patterns
  - Suggests targeted remediation
============================================================
"""

import logging

logger = logging.getLogger(__name__)


async def detect_misconception(
    concept: str,
    student_answer: str,
    correct_answer: str | None = None,
    question_type: str = "mcq",
) -> dict:
    """
    Analyze an incorrect answer to identify the likely misconception.

    ============================================================
    PLACEHOLDER: Returns a generic misconception based on the concept.
    Replace with LLM-powered misconception analysis when configured.
    ============================================================

    Returns:
        {
            "misconception": str,
            "affected_concept": str,
            "remediation_strategy": str,
            "confidence": float,
        }
    """
    logger.warning(
        "PLACEHOLDER: Using generic misconception detection. "
        "Configure LLM_API_KEY for precise analysis."
    )

    return {
        "misconception": f"Likely misunderstanding of the core principle of {concept}",
        "affected_concept": concept,
        "remediation_strategy": _select_remediation(concept),
        "confidence": 0.7,
    }


def _select_remediation(concept: str) -> str:
    """
    Select a remediation strategy.

    Strategies per Team 3 spec:
    - re_explain: Explain again with different wording
    - analogy: Use an everyday analogy
    - worked_example: Walk through a step-by-step example
    - visual: Show a diagram or visual
    - simplify: Break down into simpler sub-concepts
    """
    # Simple rotation of strategies for placeholder
    strategies = [
        "analogy",
        "worked_example",
        "visual",
        "simplify",
        "re_explain",
    ]
    # Deterministic selection based on concept name length
    idx = len(concept) % len(strategies)
    return strategies[idx]
