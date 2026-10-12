"""Deterministic exercise grading.

Grading is local and never uses AI, because free users need it and AI is
premium. It runs on the server so correct answers never reach the client (they
would be easy to read there); an answer is only revealed after an attempt.

Matching ignores things that shouldn't count as mistakes at A1 (case, extra
whitespace, trailing punctuation) but is strict about the German itself.
Umlauts and ß are kept, since "schon" and "schön" are different words.
"""

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


def _accepted_answers(exercise: Exercise) -> list[str]:
    """A simple exercise may list alternatives separated by '|'."""
    return [a for a in (exercise.correct_answer or "").split("|") if a.strip()]


def grade(exercise: Exercise, answer) -> bool:
    """True if `answer` solves `exercise`. Unknown types never pass silently."""
    etype = exercise.exercise_type

    if etype == "multiple_choice":
        return normalize(answer) == normalize(exercise.payload.get("answer", ""))

    if etype == "sentence_order":
        expected = exercise.payload.get("answer", [])
        if not isinstance(answer, (list, tuple)):
            return False
        if len(answer) != len(expected):
            return False
        return [normalize(t) for t in answer] == [normalize(t) for t in expected]

    if etype == "word_bank":
        expected = exercise.payload.get("answers", [])
        if not isinstance(answer, (list, tuple)) or len(answer) != len(expected):
            return False
        return [normalize(t) for t in answer] == [normalize(t) for t in expected]

    if etype == "matching":
        pairs = exercise.payload.get("pairs", [])
        if not isinstance(answer, dict):
            return False
        return all(normalize(answer.get(left, "")) == normalize(right) for left, right in pairs)

    if etype in {"translation", "fill_blank", "article", "conjugation"}:
        given = normalize(answer)
        return any(given == normalize(a) for a in _accepted_answers(exercise))

    # free_text has no single right answer and needs AI, so it can't be graded here.
    return False


def public_exercise(exercise: Exercise) -> dict:
    """An exercise as the client may see it, with the answers removed.

    The lesson player and the level exam both use this, so there is one place
    that decides what is safe to send.
    """
    payload = dict(exercise.payload or {})
    payload.pop("answer", None)
    payload.pop("answers", None)
    if exercise.exercise_type == "matching":
        pairs = payload.pop("pairs", [])
        payload["left"] = [p[0] for p in pairs]
        payload["right"] = sorted({p[1] for p in pairs})
    return {
        "exercise_id": exercise.id,
        "type": exercise.exercise_type,
        "prompt": exercise.prompt,
        "hint": exercise.hint,
        "payload": payload,
    }


def solution_of(exercise: Exercise):
    """The answer to reveal *after* an attempt (never before)."""
    etype = exercise.exercise_type
    if etype == "multiple_choice":
        return exercise.payload.get("answer", "")
    if etype == "sentence_order":
        return exercise.payload.get("answer", [])
    if etype == "word_bank":
        return exercise.payload.get("answers", [])
    if etype == "matching":
        return exercise.payload.get("pairs", [])
    return _accepted_answers(exercise)[:1] or [""]
