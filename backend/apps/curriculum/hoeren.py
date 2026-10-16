"""Hören: exam-style listening, one set per Modul (like the Goethe exam's "Hören").

A1 like Start Deutsch 1 (dialogues, announcements, phone messages), written in
`content/<level>/hoeren.py`. Each Teil is a `group` exercise; a recording
(`clip`: a script of up to two speakers and how often it may be played) sits on
a question or on the whole Teil. The audio is generated once from the scripts
(`manage.py make_hoeren_audio`) into the frontend's `public/hoeren/`, and the
files that exist are listed in `content/hoeren_audio.json`, so a set only shows
once all its audio is there. Grading, unlocking and best scores are Lesen's;
the scripts are sent only after answering, as transcripts.
"""

import json
from pathlib import Path

from django.conf import settings

from . import grading, lesen
from .content.levels import LEVELS
from .exam_sets import SetNotFound, open_set, open_teil, parse_source, set_source

SKILL = "hoeren"
MANIFEST = Path(__file__).parent / "content" / "hoeren_audio.json"
AUDIO_URL = "/hoeren/{}.mp3"


def _clips(source: str, whole, parts) -> list[tuple[str, dict]]:
    if whole:
        return [(f"{source}-all", whole)]
    return [(f"{source}-{i}", p["clip"]) for i, p in enumerate(parts) if p.get("clip")]


def clips_of(exercise) -> list[tuple[str, dict]]:
    """(file name, clip) of every recording in a Teil: "<source>-all" for one
    recording for the whole Teil, "<source>-<n>" for question n's."""
    return _clips(exercise.source, (exercise.payload or {}).get("clip"), grading.parts_of(exercise))


def content_clips(level: str, modul: int, teil: int, item: dict) -> list[tuple[str, dict]]:
    """The same names, straight from the content files (for the audio generator)."""
    return _clips(set_source(SKILL, level, modul, teil), item.get("clip"), item["parts"])


def available() -> set[str]:
    """The recordings whose audio file has been generated."""
    try:
        return set(json.loads(MANIFEST.read_text()))
    except FileNotFoundError:
        return set()


def _complete(teile) -> bool:
    """A set goes live once it's released (`LIVE` in its content file) and all its
    audio exists. Locally (DEBUG) every set shows, recorded or not."""
    if settings.DEBUG:
        return True
    _, level, modul, _ = parse_source(teile[0][1].source)
    if modul not in LEVELS[level].get("hoeren_live", set()):
        return False
    have = available()
    return all(name in have for _, e in teile for name, _ in clips_of(e))


def _audio(name: str, recording: dict) -> dict:
    return {"url": AUDIO_URL.format(name), "plays": recording["plays"]}


def public_teil(exercise) -> dict:
    """A Teil without answers or scripts, with the audio and how often it may play."""
    out = grading.public_exercise(exercise)
    clips = clips_of(exercise)
    if (exercise.payload or {}).get("clip"):
        out["payload"]["audio"] = _audio(*clips[0])
    else:
        by_part = dict(clips)
        for i, part in enumerate(out["payload"]["parts"]):
            name = f"{exercise.source}-{i}"
            if name in by_part:
                part["payload"]["audio"] = _audio(name, by_part[name])
    return out


def _transcript(recording: dict) -> str:
    return "\n".join(f"{speaker}: {line}" for speaker, line in recording["script"])


def status(user) -> list[dict]:
    return lesen.status(user, SKILL, keep=_complete)


def detail(user, level: str, modul: int) -> dict:
    if not _complete(open_set(user, SKILL, level, modul)):
        raise SetNotFound("This listening set isn't recorded yet.")
    return lesen.detail(user, level, modul, SKILL, public=public_teil)


def answer(user, exercise_id: int, given) -> dict:
    """Grade a Teil like Lesen and add the transcripts (one per recording)."""
    exercise, _ = open_teil(user, SKILL, exercise_id)
    if not _complete([(0, exercise)]):
        raise SetNotFound("This listening set isn't recorded yet.")
    result = lesen.answer(user, exercise_id, given, SKILL)
    payload = exercise.payload or {}
    if payload.get("clip"):
        result["transcripts"] = [_transcript(payload["clip"])]
    else:
        result["transcripts"] = [
            _transcript(p["clip"]) if p.get("clip") else "" for p in grading.parts_of(exercise)
        ]
    return result
