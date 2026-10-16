"""Schreiben: exam-style writing, one set per Modul, scored like the Goethe exams.

* **A1** (Start Deutsch 1), 15 points: Teil 1 a form with five gaps from a short
  text (1 point each, graded locally); Teil 2 a short message on three points,
  3 / 1.5 / 0 each, plus communicative design 1 / 0.5 / 0 (greeting, sign-off).
* **A2** (Goethe A2), 20 points: Teil 1 an informal SMS (20-30 words), Teil 2 a
  semi-formal e-mail (30-40 words), three points each, graded A-E
  (5 / 3.5 / 2 / 0.5 / 0) on task fulfilment and on language. Under half the
  minimum words gives 0 for the Teil.

Free text can't be graded deterministically, so: everyone gets the local
checks (word count, greeting, sign-off) and a model answer, then rates each of
the three points themselves; premium users can have Gemini grade the text on
the official criteria (`llm.grade_writing`). Gemini only labels the grades;
the score always comes from the rubric below. Sets, sources and unlocking are
shared with Lesen (`exam_sets`). Every attempt is kept (`WritingAttempt`).
"""

import re

from apps.ai_assistant import llm

from . import grading
from .exam_sets import PASS_SHARE, header, open_set, open_teil, visible_sets
from .models import WritingAttempt

SKILL = "schreiben"
WRITING_FIELDS = ("situation", "points", "min_words", "max_words", "formal", "model")
MAX_TEXT = 2000  # characters; the exam texts are 20-40 words
GRADES = ("full", "partial", "missing")
POINT_SCORE = {"full": 3, "partial": 1.5, "missing": 0}  # A1, per content point
LETTER_SCORE = {"A": 5, "B": 3.5, "C": 2, "D": 0.5, "E": 0}  # A2, per criterion

_WORD = re.compile(r"[0-9A-Za-zÄÖÜäöüß]+(?:[-'][0-9A-Za-zÄÖÜäöüß]+)*")
_GREETING = re.compile(
    r"^\s*(hallo|hi|hey|liebe[rs]?|sehr geehrte[rs]?|guten (tag|morgen|abend))\b", re.I
)
# A sign-off in the last two lines: "Viele Grüße", "Bis bald", "Danke, Nora", "Deine Sara".
_CLOSING = re.compile(
    r"(grüße|gruß|bis (bald|später|dann|gleich|morgen)|tschüs+|ciao|\blg\b|danke"
    r"|^\s*(dein|deine|euer|eure|ihr|ihre)\b)",
    re.I | re.M,
)


class WritingError(Exception):
    """A request that doesn't fit the task (bad text, wrong Teil, already graded)."""


# ---- the rubric (pure) -------------------------------------------------------


def count_words(text: str) -> int:
    return len(_WORD.findall(text))


def checks(text: str, task: dict) -> dict:
    """What can be checked without reading for meaning."""
    lines = [line for line in text.strip().splitlines() if line.strip()]
    words = count_words(text)
    return {
        "words": words,
        "min_words": task["min_words"],
        "max_words": task["max_words"],
        "in_range": task["min_words"] <= words <= task["max_words"],
        # The exam gives 0 under half the minimum (A2: 10 words in Teil 1, 15 in Teil 2).
        "too_short": words < task["min_words"] / 2,
        "greeting": bool(lines and _GREETING.search(lines[0])),
        "closing": len(lines) > 1 and bool(_CLOSING.search("\n".join(lines[-2:]))),
    }


def a1_score(points: list[str], check: dict) -> tuple[float, float, dict]:
    """A1 Teil 2: (score, max, detail). 3 / 1.5 / 0 per point + communication."""
    if check["too_short"]:
        return 0, 10, {"communication": 0}
    communication = (check["greeting"] + check["closing"]) / 2
    return sum(POINT_SCORE[p] for p in points) + communication, 10, {"communication": communication}


def a2_task_letter(points: list[str]) -> str:
    """A2 task fulfilment from the three points, as in the official table."""
    full, partial = points.count("full"), points.count("partial")
    if full == 3:
        return "A"
    if full == 2 or (full == 1 and partial == 2):
        return "B"
    if (full == 1 and partial == 1) or partial == 3:
        return "C"
    if full + partial >= 1:
        return "D"
    return "E"


def a2_score(points: list[str], check: dict, language: str | None) -> tuple[float, float, dict]:
    """A2 Teil: (score, max, detail). Without a language grade (self-check)
    only task fulfilment is scored, out of 5."""
    task = "E" if check["too_short"] else a2_task_letter(points)
    out_of = 10 if language else 5
    if task == "E":  # the exam then gives 0 for the whole Teil
        return 0, out_of, {"task": "E", "language": language and "E"}
    score = LETTER_SCORE[task] + (LETTER_SCORE[language] if language else 0)
    return score, out_of, {"task": task, "language": language}


def score(level: str, points: list[str], check: dict, language: str | None = None):
    if level == "A1":
        return a1_score(points, check)
    return a2_score(points, check, language)


# ---- sets and attempts ---------------------------------------------------------


def _task(exercise) -> dict:
    return {k: exercise.payload.get(k) for k in WRITING_FIELDS}


def public_teil(exercise) -> dict:
    """A Teil as the client may see it: never the form's answers or the model text."""
    if exercise.exercise_type == "group":
        return grading.public_exercise(exercise)
    task = _task(exercise)
    task.pop("model")
    return {
        "exercise_id": exercise.id,
        "type": "free_text",
        "prompt": exercise.prompt,
        "hint": "",
        "payload": task,
    }


def _best(user) -> dict[int, WritingAttempt]:
    """The best graded attempt per Teil (by share of points)."""
    best: dict[int, WritingAttempt] = {}
    for a in WritingAttempt.objects.filter(user=user, score__isnull=False):
        b = best.get(a.exercise_id)
        if b is None or a.score / (a.max_score or 1) > b.score / (b.max_score or 1):
            best[a.exercise_id] = a
    return best


def _set_score(teile, best) -> dict:
    done = [best.get(e.id) for _, e in teile]
    if not all(done):
        return {"best": None, "out_of": None, "passed": False}
    got, out_of = sum(a.score for a in done), sum(a.max_score for a in done)
    return {"best": got, "out_of": out_of, "passed": got >= PASS_SHARE * out_of}


def _teil_best(best, exercise) -> dict | None:
    a = best.get(exercise.id)
    return {"score": a.score, "out_of": a.max_score, "graded_by": a.graded_by} if a else None


def status(user) -> list[dict]:
    best = _best(user)
    return [
        {
            **header(level, modul),
            "locked": locked,
            **_set_score(teile, best),
            "teile": [
                {"id": e.id, "teil": teil, "title": e.prompt, "best": _teil_best(best, e)}
                for teil, e in teile
            ],
        }
        for level, modul, teile, locked in visible_sets(user, SKILL)
    ]


def detail(user, level: str, modul: int) -> dict:
    teile = open_set(user, SKILL, level, modul)
    best = _best(user)
    return {
        **header(level.upper(), modul),
        "pass_share": PASS_SHARE,
        **_set_score(teile, best),
        "teile": [
            {"teil": teil, "best": _teil_best(best, e), **public_teil(e)} for teil, e in teile
        ],
    }


def attempt_payload(a: WritingAttempt) -> dict:
    return {
        "id": a.id,
        "exercise_id": a.exercise_id,
        "answer": a.answer,
        "words": a.words,
        "points": a.points,
        "score": a.score,
        "max_score": a.max_score,
        "graded_by": a.graded_by,
        "feedback": a.feedback,
        "created_at": a.created_at.isoformat(),
    }


def answer_form(user, exercise_id: int, given) -> dict:
    """A1 Teil 1: grade the form locally, keep the attempt, reveal the solution."""
    exercise, _ = open_teil(user, SKILL, exercise_id)
    if exercise.exercise_type != "group":
        raise WritingError("This Teil is free writing.")
    verdicts = grading.grade_parts(exercise, given)
    attempt = WritingAttempt.objects.create(
        user=user,
        exercise=exercise,
        answer=given if isinstance(given, list) else [],
        score=sum(verdicts),
        max_score=len(verdicts),
        graded_by=WritingAttempt.GradedBy.AUTO,
    )
    return {
        "correct": all(verdicts),
        "parts": verdicts,
        "solution": grading.solution_of(exercise),
        "explanation": exercise.explanation,
        "attempt": attempt_payload(attempt),
    }


def write(user, exercise_id: int, text) -> dict:
    """Keep a written text and return the checks, the points and the model answer.
    A text under half the minimum is scored 0 at once, as in the exam."""
    exercise, key = open_teil(user, SKILL, exercise_id)
    if exercise.exercise_type != "free_text":
        raise WritingError("This Teil is a form.")
    if not isinstance(text, str) or not text.strip():
        raise WritingError("Write your text first.")
    if len(text) > MAX_TEXT:
        raise WritingError(f"Keep it under {MAX_TEXT} characters.")
    task = _task(exercise)
    check = checks(text, task)
    attempt = WritingAttempt(
        user=user, exercise=exercise, answer=text.strip(), words=check["words"]
    )
    attempt.feedback = {"checks": check}
    if check["too_short"]:
        attempt.points = ["missing"] * 3
        attempt.score, attempt.max_score, detail_ = score(key[1], attempt.points, check)
        attempt.feedback["grades"] = detail_
        attempt.graded_by = WritingAttempt.GradedBy.AUTO
    attempt.save()
    return {"attempt": attempt_payload(attempt), "points": task["points"], "model": task["model"]}


def _own_attempt(user, attempt_id: int) -> tuple[WritingAttempt, tuple]:
    attempt = WritingAttempt.objects.filter(id=attempt_id, user=user).first()
    if attempt is None:
        raise WritingError("No such attempt.")
    exercise, key = open_teil(user, SKILL, attempt.exercise_id)
    if exercise.exercise_type != "free_text":
        raise WritingError("This Teil is a form.")
    return attempt, key


def self_check(user, attempt_id: int, points) -> dict:
    """Score a text from the user's own rating of the three points."""
    attempt, key = _own_attempt(user, attempt_id)
    if attempt.graded_by:
        raise WritingError("This text is already graded.")
    if not (isinstance(points, list) and len(points) == 3 and all(p in GRADES for p in points)):
        raise WritingError("Rate each of the three points.")
    check = attempt.feedback.get("checks") or checks(attempt.answer, _task(attempt.exercise))
    attempt.points = points
    attempt.score, attempt.max_score, detail_ = score(key[1], points, check)
    attempt.feedback = {**attempt.feedback, "grades": detail_}
    attempt.graded_by = WritingAttempt.GradedBy.SELF
    attempt.save()
    return attempt_payload(attempt)


def ai_grade(user, attempt_id: int) -> dict:
    """Premium: Gemini grades the text on the exam's criteria; the rubric scores it.
    Raises llm.AIConfigError without a key (the view answers 503)."""
    attempt, key = _own_attempt(user, attempt_id)
    if attempt.graded_by == WritingAttempt.GradedBy.AI:
        raise WritingError("This text is already graded by AI.")
    task = _task(attempt.exercise)
    result = llm.grade_writing(key[1], attempt.exercise.prompt, task, attempt.answer)
    check = attempt.feedback.get("checks") or checks(attempt.answer, task)
    points = result["points"]
    attempt.points = points
    if key[1] == "A1":
        attempt.score, attempt.max_score, detail_ = score("A1", points, check)
    else:
        attempt.score, attempt.max_score, detail_ = score("A2", points, check, result["language"])
    attempt.feedback = {
        **attempt.feedback,
        "grades": detail_,
        "comments": result["comments"],
        "corrected": result["corrected"],
        "tips": result["tips"],
    }
    attempt.graded_by = WritingAttempt.GradedBy.AI
    attempt.save()
    return attempt_payload(attempt)


def attempts(user, exercise_id: int) -> list[dict]:
    """The user's past attempts at one Teil, newest first."""
    exercise, _ = open_teil(user, SKILL, exercise_id)
    rows = WritingAttempt.objects.filter(user=user, exercise=exercise)[:20]
    return [attempt_payload(a) for a in rows]
