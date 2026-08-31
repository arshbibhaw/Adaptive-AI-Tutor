"""
Video API endpoints.

POST /video/generate — Generate a teaching video for a segment.
GET  /video/status/{segment_id} — Check video generation status.
"""

import logging

from fastapi import APIRouter, Depends

from backend.app.core.dependencies import get_current_user_id
from backend.app.schemas.video import VideoGenerateRequest, VideoResult, VideoStatusResponse
from backend.app.services.video.video_generator import generate_teaching_video

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate", response_model=VideoResult)
async def generate_video(
    data: VideoGenerateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Generate a teaching video for a lesson segment.

    ============================================================
    PLACEHOLDER: Video pipeline returns placeholder results.
    Real video generation requires TTS and Avatar API keys.
    ============================================================
    """
    result = await generate_teaching_video(
        segment_id=data.segment_id,
        script=data.script,
        concept=data.segment_id,
        visual_type=data.visual_type,
        language=data.language,
    )
    return result


@router.get("/status/{segment_id}", response_model=VideoStatusResponse)
async def get_video_status(
    segment_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """
    Get the status of a video generation.

    ============================================================
    PLACEHOLDER: Always returns placeholder status.
    ============================================================
    """
    logger.warning("PLACEHOLDER: Video status check for segment %s.", segment_id)

    return VideoStatusResponse(
        segment_id=segment_id,
        status="placeholder",
        video_url=None,
        duration_seconds=None,
    )
