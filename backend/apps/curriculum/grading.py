"""Deterministic exercise grading.

Grading is local and never uses AI, because free users need it and AI is
premium. It runs on the server so correct answers never reach the client (they
would be easy to read there); an answer is only revealed after an attempt.

Matching ignores things that shouldn't count as mistakes at A1 (case, extra
whitespace, trailing punctuation) but is strict about the German itself.
Umlauts and ß are kept, since "schon" and "schön" are different words.
"""

import base64
import re
import unicodedata

from apps.exercises.models import Exercise

_PUNCT_EDGES = re.compile(r"^[\s\"'“”„»«]+|[\s\.\!\?\,\;\:\"'“”„»«]+$")


def normalize(text: str) -> str:
    """Casefold + collapse whitespace + trim edge punctuation. Keeps umlauts/ß."""
    text = unicodedata.normalize("NFC", str(text))
    text = _PUNCT_EDGES.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().casefold()


SIMPLE_TYPES = {"translation", "fill_blank", "article", "conjugation", "dictation"}
_ANY_PUNCT = re.compile(r"[^\w\s]")


def _loose(text: str) -> str:
    """For dictation: punctuation anywhere doesn't count, only the words."""
    return normalize(_ANY_PUNCT.sub(" ", unicodedata.normalize("NFC", str(text))))


def encode_speech(text: str) -> str:
    """Text the browser reads aloud (dictation, "which word do you hear?").
    It has to reach the client, so it's only encoded, to keep it from being
    readable at a glance in the page data."""
    return base64.b64encode(text.encode()).decode()


def parts_of(exercise: Exercise) -> list[dict]:
    """An exercise as a list of parts, each `{"type", "prompt", "hint", ...}`
    with its answer fields (the shape the content files use).

    A `group` exercise stores its parts in `payload["parts"]`; any other
    exercise is a single part. Simple types keep their answer in the
    `correct_answer` column, so it is copied in as `answer`.
    """
    if exercise.exercise_type == "group":
        return list((exercise.payload or {}).get("parts", []))
    part = {
        "type": exercise.exercise_type,
        "prompt": exercise.prompt,
        "hint": exercise.hint,
        **(exercise.payload or {}),
    }
    if exercise.exercise_type in SIMPLE_TYPES:
        part["answer"] = exercise.correct_answer or ""
    return [part]


def _accepted(part: dict) -> list[str]:
    """A simple part may list alternatives separated by '|'."""
    return [a for a in (part.get("answer") or "").split("|") if a.strip()]


def _same_list(answer, expected) -> bool:
    if not isinstance(answer, (list, tuple)) or len(answer) != len(expected):
        return False
    return [normalize(t) for t in answer] == [normalize(t) for t in expected]


def grade_part(part: dict, answer) -> bool:
    """True if `answer` solves one part. Unknown types never pass silently."""
    ptype = part.get("type")
    if ptype == "multiple_choice":
        return normalize(answer) == normalize(part.get("answer", ""))
    if ptype == "sentence_order":
        return _same_list(answer, part.get("answer", []))
    if ptype == "word_bank":
        return _same_list(answer, part.get("answers", []))
    if ptype == "error_spot":
        return str(answer) == str(part.get("answer"))
    if ptype == "dictation":
        if not isinstance(answer, str):
            return False
        given = _loose(answer)
        return bool(given) and any(given == _loose(a) for a in _accepted(part))
    if ptype == "matching":
        if not isinstance(answer, dict):
            return False
        return all(
            normalize(answer.get(left, "")) == normalize(right)
            for left, right in part.get("pairs", [])
        )
    if ptype in SIMPLE_TYPES:
        given = normalize(answer)
        return any(given == normalize(a) for a in _accepted(part))
    # free_text has no single right answer and needs AI, so it can't be graded here.
    return False


def grade_parts(exercise: Exercise, answer) -> list[bool]:
    """One verdict per part. A group's answer is a list with one entry per part."""
    parts = parts_of(exercise)
    if exercise.exercise_type != "group":
        return [grade_part(parts[0], answer)]
    answers = answer if isinstance(answer, (list, tuple)) else []
    return [grade_part(p, answers[i] if i < len(answers) else None) for i, p in enumerate(parts)]


def public_part(part: dict) -> dict:
    """A part as the client may see it, with the answers removed."""
    payload = {
        k: v
        for k, v in part.items()
        if k
        not in ("type", "prompt", "hint", "explanation", "answer", "answers", "correction", "say")
    }
    if part.get("say"):  # a word to hear, set by the checks
        payload["say"] = encode_speech(part["say"])
    if part.get("type") == "dictation":
        payload["say"] = encode_speech(_accepted(part)[0])
    if part.get("type") == "matching":
        pairs = payload.pop("pairs", [])
        payload["left"] = [p[0] for p in pairs]
        payload["right"] = sorted({p[1] for p in pairs})
    return {
        "type": part.get("type"),
        "prompt": part.get("prompt", ""),
        "hint": part.get("hint", ""),
        "payload": payload,
    }


def public_exercise(exercise: Exercise) -> dict:
    """An exercise as the client may see it, with the answers removed.

    The lesson player and the level exam both use this, so there is one place
    that decides what is safe to send. A group's parts go in `payload.parts`.
    """
    if exercise.exercise_type == "group":
        out = {
            "type": "group",
            "prompt": exercise.prompt,
            "hint": exercise.hint,
            "payload": {"parts": [public_part(p) for p in parts_of(exercise)]},
        }
        if (exercise.payload or {}).get("context"):
            out["payload"]["context"] = exercise.payload["context"]
    else:
        out = public_part(parts_of(exercise)[0])
    return {"exercise_id": exercise.id, **out}


def solution_of_part(part: dict):
    """The answer to reveal for one part *after* an attempt (never before)."""
    ptype = part.get("type")
    if ptype in ("multiple_choice", "sentence_order"):
        return part.get("answer", "" if ptype == "multiple_choice" else [])
    if ptype == "word_bank":
        return part.get("answers", [])
    if ptype == "matching":
        return part.get("pairs", [])
    if ptype == "error_spot":
        return [str(part.get("answer", "")), part.get("correction", "")]
    return _accepted(part)[:1] or [""]


def solution_of(exercise: Exercise):
    """The answer to reveal *after* an attempt. A group gives one per part."""
    parts = parts_of(exercise)
    if exercise.exercise_type == "group":
        return [solution_of_part(p) for p in parts]
    return solution_of_part(parts[0])
