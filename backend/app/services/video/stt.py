"""
Speech-to-Text (STT) service.

============================================================
PLACEHOLDER — STT provider not yet configured.
============================================================
TODO: When the STT provider is selected (e.g., OpenAI Whisper),
implement speech-to-text transcription for voice-based student
answers. This is a P1 feature.

Candidate providers:
  - OpenAI Whisper API
  - Google Speech-to-Text
  - Azure Speech Services
============================================================
"""

import logging

logger = logging.getLogger(__name__)


async def transcribe_audio(
    audio_path: str,
    language: str = "en",
) -> dict:
    """
    Transcribe audio to text.

    ============================================================
    PLACEHOLDER: Returns empty transcription.
    This is a P1 feature — not required for hackathon MVP.
    ============================================================
    """
    logger.warning(
        "PLACEHOLDER: STT not configured. This is a P1 feature."
    )

    return {
        "text": "",
        "language": language,
        "confidence": 0.0,
    }
