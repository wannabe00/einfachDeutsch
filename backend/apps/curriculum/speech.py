"""Recorded German for the listening tasks ("what do you hear?", dictation).

Each text is recorded once by `make_speech_audio` (Azure, German voice) into
frontend/public/speech/, which Vercel serves as static files, so nothing is
stored or paid per play. `content/speech_audio.json` lists what exists; a text
without a recording falls back to the browser's own speech.
"""

import hashlib
import json
from pathlib import Path

MANIFEST = Path(__file__).parent / "content" / "speech_audio.json"


def clip_name(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()[:16]


def _recorded() -> set[str]:
    try:
        return set(json.loads(MANIFEST.read_text()))
    except FileNotFoundError:
        return set()


RECORDED = _recorded()


def audio_url(text: str) -> str | None:
    name = clip_name(text)
    return f"/speech/{name}.mp3" if name in RECORDED else None


def spoken_text(part: dict) -> str:
    """What the browser reads aloud for a part: its `say`, or a dictation's answer."""
    if part.get("say"):
        return part["say"]
    if part.get("type") == "dictation":
        answers = [a for a in (part.get("answer") or "").split("|") if a.strip()]
        return answers[0] if answers else ""
    return ""
