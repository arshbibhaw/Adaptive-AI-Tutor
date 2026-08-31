"""
Text-to-Speech (TTS) service.

============================================================
PLACEHOLDER — TTS provider not yet configured.
============================================================
TODO: When the TTS provider is selected (e.g., ElevenLabs,
edge-tts, gTTS), implement the following:
  - Text to audio conversion
  - Language/voice selection
  - Speaking speed control
  - Subtitle/transcript generation from timing data
  - Audio file storage and URL generation

Candidate providers:
  - ElevenLabs (high quality, paid)
  - edge-tts (free, Microsoft voices)
  - gTTS (free, Google voices)
  - OpenAI TTS (good quality, paid)
============================================================
"""

import logging

logger = logging.getLogger(__name__)


async def generate_speech(
    text: str,
    language: str = "en",
    voice_id: str | None = None,
    speed: float = 1.0,
) -> dict:
    """
    Convert text to speech audio.

    ============================================================
    PLACEHOLDER: Returns a mock audio result.
    Replace with actual TTS API call when provider is configured.
    ============================================================

    Returns:
        {
            "audio_url": str,
            "duration_seconds": float,
            "language": str,
            "subtitles": list[dict],
        }
    """
    logger.warning(
        "PLACEHOLDER: TTS not configured. Configure TTS_API_KEY for audio generation."
    )

    # Estimate duration: ~150 words per minute average
    word_count = len(text.split())
    estimated_duration = (word_count / 150.0) * 60.0 / speed

    return {
        "audio_url": "",
        "duration_seconds": round(estimated_duration, 1),
        "language": language,
        "subtitles": _generate_placeholder_subtitles(text),
    }


def _generate_placeholder_subtitles(text: str) -> list[dict]:
    """Generate placeholder subtitle entries from text."""
    sentences = text.replace(".", ".|").replace("!", "!|").replace("?", "?|").split("|")
    subtitles = []
    current_time = 0.0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        word_count = len(sentence.split())
        duration = (word_count / 150.0) * 60.0
        subtitles.append({
            "text": sentence,
            "start": round(current_time, 1),
            "end": round(current_time + duration, 1),
        })
        current_time += duration

    return subtitles
