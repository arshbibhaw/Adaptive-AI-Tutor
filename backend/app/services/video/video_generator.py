"""
Video generator service.

Orchestrates the video pipeline per Team 4 spec:
Lesson Segment → Script → Visual Plan → TTS → Avatar → Visual composition → Final video.

============================================================
PLACEHOLDER — Video pipeline not fully configured.
============================================================
TODO: When TTS and Avatar providers are configured, this
pipeline will produce real teaching videos. Currently returns
placeholder results with estimated durations.
============================================================
"""

import logging
import uuid

from backend.app.schemas.video import VideoResult
from backend.app.services.video.tts import generate_speech
from backend.app.services.video.avatar import generate_avatar_video
from backend.app.services.video.visuals import generate_visual

logger = logging.getLogger(__name__)


async def generate_teaching_video(
    segment_id: str,
    script: str,
    concept: str,
    visual_type: str = "diagram",
    language: str = "en",
) -> VideoResult:
    """
    Generate a complete teaching video for a lesson segment.

    Pipeline: Script → TTS → Avatar → Visuals → Compose.

    ============================================================
    PLACEHOLDER: Runs the pipeline but all sub-services return
    placeholder results. Replace when providers are configured.
    ============================================================
    """
    logger.info(
        "Generating teaching video for segment %s (concept: %s, visual: %s).",
        segment_id, concept, visual_type,
    )

    # Step 1: Generate speech audio
    tts_result = await generate_speech(script, language=language)

    # Step 2: Generate avatar video
    avatar_result = await generate_avatar_video(
        script=script,
        audio_url=tts_result.get("audio_url"),
        language=language,
    )

    # Step 3: Generate visual
    visual_result = await generate_visual(
        concept=concept,
        visual_type=visual_type,
        explanation=script,
        language=language,
    )

    # Step 4: Compose final video (placeholder — just combine results)
    video_url = avatar_result.get("video_url", "")
    duration = max(
        tts_result.get("duration_seconds", 0),
        avatar_result.get("duration_seconds", 0),
    )

    status = "completed" if video_url else "placeholder"

    logger.info(
        "Video generation %s for segment %s (duration: %ds).",
        status, segment_id, duration,
    )

    return VideoResult(
        segment_id=segment_id,
        status=status,
        video_url=video_url,
        duration_seconds=int(duration),
        language=language,
    )
