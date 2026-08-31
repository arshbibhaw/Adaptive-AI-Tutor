"""
Video schemas.

Pydantic models for the VideoResult shared contract.
"""

from pydantic import BaseModel


class VideoResult(BaseModel):
    """
    Shared VideoResult contract.

    Used by: Video (Team 4), Frontend (Team 5), Backend (Team 6).
    """
    segment_id: str
    status: str  # pending | generating | completed | failed
    video_url: str = ""
    duration_seconds: int = 0
    language: str = "en"


class VideoGenerateRequest(BaseModel):
    """Request to generate a teaching video for a lesson segment."""
    session_id: str
    segment_id: str
    script: str
    visual_type: str = "none"
    language: str = "en"


class VideoStatusResponse(BaseModel):
    """Response containing the current status of a video generation."""
    segment_id: str
    status: str
    video_url: str | None = None
    duration_seconds: int | None = None
