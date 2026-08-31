"""
Subject-aware visual engine.

Produces visual descriptions/references based on subject type per Team 4 spec:
  - Math → equations / graphs / worked steps
  - Physics → diagrams / formulas / processes
  - Biology → structures / labels / processes
  - History → timelines / maps / events
  - Programming → code / output / execution flow
  - AI/ML → architectures / graphs / pipelines

============================================================
PLACEHOLDER — Visual generation not yet configured.
============================================================
TODO: When configured, integrate with:
  - LLM for generating visual descriptions and code
  - Image generation API for diagrams
  - LaTeX rendering for equations
  - Chart libraries for graphs
============================================================
"""

import logging

logger = logging.getLogger(__name__)


async def generate_visual(
    concept: str,
    visual_type: str,
    explanation: str = "",
    language: str = "en",
) -> dict:
    """
    Generate a subject-aware visual for a concept.

    ============================================================
    PLACEHOLDER: Returns a visual description.
    Replace with actual visual generation when configured.
    ============================================================

    Returns:
        {
            "visual_type": str,
            "description": str,
            "content": str,
            "url": str | None,
        }
    """
    logger.warning(
        "PLACEHOLDER: Visual generation not configured. Returning descriptions only."
    )

    visual_content = _get_visual_content(concept, visual_type)

    return {
        "visual_type": visual_type,
        "description": visual_content["description"],
        "content": visual_content["content"],
        "url": None,
    }


def _get_visual_content(concept: str, visual_type: str) -> dict:
    """Generate placeholder visual content based on type."""
    templates = {
        "equation": {
            "description": f"Mathematical equation for {concept}",
            "content": f"[Equation: {concept}]",
        },
        "diagram": {
            "description": f"Diagram illustrating {concept}",
            "content": f"[Diagram: {concept}]",
        },
        "graph": {
            "description": f"Graph showing {concept} relationships",
            "content": f"[Graph: {concept}]",
        },
        "timeline": {
            "description": f"Timeline of events for {concept}",
            "content": f"[Timeline: {concept}]",
        },
        "code": {
            "description": f"Code example for {concept}",
            "content": f"# Code: {concept}\n# TODO: Add implementation",
        },
        "none": {
            "description": f"Visual for {concept}",
            "content": "",
        },
    }
    return templates.get(visual_type, templates["diagram"])
