"""Speech→text for recitation, behind a swappable interface (Phase 16.2).

Default impl uses Gemini multimodal (the project's free key). A paid Whisper /
Azure transcriber can be dropped in later by implementing `Transcriber` and
returning it from `get_transcriber()` — no caller changes needed.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from django.conf import settings
from google import genai
from google.genai import types

from apps.ai_assistant.llm import MODEL, AIConfigError


class Transcriber(ABC):
    @abstractmethod
    def transcribe(self, audio: bytes, mime_type: str) -> str:
        """Return the German transcription of the given audio bytes."""


class GeminiTranscriber(Transcriber):
    def transcribe(self, audio: bytes, mime_type: str) -> str:
        key = settings.GEMINI_API_KEY
        if not key:
            raise AIConfigError("GEMINI_API_KEY is not set.")
        client = genai.Client(api_key=key)
        resp = client.models.generate_content(
            model=MODEL,
            contents=[
                "Transcribe this German speech to text, verbatim. "
                "Output ONLY the transcription — no commentary, no quotes.",
                types.Part.from_bytes(data=audio, mime_type=mime_type),
            ],
        )
        return (resp.text or "").strip()


def get_transcriber() -> Transcriber:
    """The active transcriber. Swap here (or via a setting) for a paid one."""
    return GeminiTranscriber()
