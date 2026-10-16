"""Lesen: exam-style reading, one set per Modul (like the Goethe exam's "Lesen").

A1 like Start Deutsch 1 (notes, adverts, signs), A2 like Goethe A2 (article,
board, e-mail, people and adverts). Each Teil is a seeded `group` exercise,
written in `content/<level>/lesen.py`; sets, sources and unlocking are shared
with Schreiben (`exam_sets`). Graded locally (free users too), never costs
energy. The best result per Teil is kept in `ReadingResult`.
"""

from . import grading
from .exam_sets import PASS_SHARE, header, open_set, open_teil, visible_sets
from .models import ReadingResult

SKILL = "lesen"


def _score(teile, results) -> dict:
    """Questions, best right answers (once every Teil is done) and passed."""
    total = sum(len(grading.parts_of(e)) for _, e in teile)
    done = [results.get(e.id) for _, e in teile]
    if total and all(done):
        best = sum(r.best_correct for r in done)
        return {"questions": total, "best": best, "passed": best >= PASS_SHARE * total}
    return {"questions": total, "best": None, "passed": False}


def _results(user) -> dict:
    return {r.exercise_id: r for r in ReadingResult.objects.filter(user=user)}


def status(user, skill: str = SKILL, keep=None) -> list[dict]:
    """Every set the user may see, lowest level first, with locks and best scores.
    Hören reuses this (`skill`), keeping only sets whose audio exists (`keep`)."""
    results = _results(user)
    return [
        {
            **header(level, modul),
            "locked": locked,
            **_score(teile, results),
            "teile": [
                {
                    "id": e.id,
                    "teil": teil,
                    "title": e.prompt,
                    "questions": len(grading.parts_of(e)),
                    "best": results[e.id].best_correct if e.id in results else None,
                }
                for teil, e in teile
            ],
        }
        for level, modul, teile, locked in visible_sets(user, skill)
        if keep is None or keep(teile)
    ]


def detail(user, level: str, modul: int, skill: str = SKILL, public=None) -> dict:
    """One open set: its Teile without answers (`public` shapes each Teil)."""
    teile = open_set(user, skill, level, modul)
    public = public or grading.public_exercise
    results = _results(user)
    return {
        **header(level.upper(), modul),
        "pass_share": PASS_SHARE,
        **_score(teile, results),
        "teile": [
            {
                "teil": teil,
                "best": results[e.id].best_correct if e.id in results else None,
                **public(e),
            }
            for teil, e in teile
        ],
    }


def answer(user, exercise_id: int, given, skill: str = SKILL) -> dict:
    """Grade one Teil, keep the best result and reveal the solution."""
    exercise, _ = open_teil(user, skill, exercise_id)
    verdicts = grading.grade_parts(exercise, given)
    correct = sum(verdicts)
    result, _ = ReadingResult.objects.get_or_create(user=user, exercise=exercise)
    result.correct = correct
    result.best_correct = max(result.best_correct, correct)
    result.total = len(verdicts)
    result.save()
    # The same shape as the other answer endpoints, plus the Teil's score.
    return {
        "correct": all(verdicts),
        "parts": verdicts,
        "solution": grading.solution_of(exercise),
        "explanation": exercise.explanation,
        "right": correct,
        "total": len(verdicts),
        "best": result.best_correct,
    }
