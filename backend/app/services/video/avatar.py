"""
Avatar generation service.

============================================================
PLACEHOLDER — Avatar provider not yet configured.
============================================================
TODO: When the avatar provider is selected (e.g., HeyGen, D-ID),
implement the following:
  - Pass teaching script + audio to avatar API
  - Generate talking-head teaching video
  - Handle generation status polling
  - Handle failures and timeouts
  - Return video URL and duration

Candidate providers:
  - HeyGen API (realistic avatars, paid)
  - D-ID API (talking head, paid)
  - Synthesia (enterprise, paid)
============================================================
"""

import logging

logger = logging.getLogger(__name__)


async def generate_avatar_video(
    script: str,
    audio_url: str | None = None,
    language: str = "en",
    avatar_id: str | None = None,
) -> dict:
    """
    Generate an avatar video from a teaching script.

    ============================================================
    PLACEHOLDER: Returns a mock video result.
    Replace with actual avatar API call when provider is configured.
    ============================================================

    Returns:
        {
            "video_url": str,
            "status": str,
            "duration_seconds": int,
        }
    """
    logger.warning(
        "PLACEHOLDER: Avatar not configured. Configure AVATAR_API_KEY for video generation."
    )

    word_count = len(script.split())
    estimated_duration = int((word_count / 150.0) * 60.0)

    return {
        "video_url": "",
        "status": "placeholder",
        "duration_seconds": estimated_duration,
    }


async def check_avatar_status(job_id: str) -> dict:
    """
    Check the status of an avatar video generation job.

    ============================================================
    PLACEHOLDER: Always returns completed.
    ============================================================
    """
    logger.warning("PLACEHOLDER: Avatar status check — not configured.")

    return {
        "job_id": job_id,
        "status": "placeholder",
        "video_url": "",
    }
