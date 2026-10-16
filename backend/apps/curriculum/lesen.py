"""Lesen: exam-style reading, one set per Modul (like the Goethe exam's "Lesen").

A set is the Teile of one Modul: A1 like Start Deutsch 1 (notes, adverts,
signs), A2 like Goethe A2 (article, board, e-mail, people and adverts). Each
Teil is a seeded `group` exercise with the source
`seed-<level>-lesen-m<modul>-t<teil>`, written in `content/<level>/lesen.py`.

A set opens once its Modul's three Lektionen are finished; every set of a
level below the user's is open, and levels above are never shown. Graded
locally (free users too), never costs energy. The best result per Teil is kept
in `ReadingResult`; a set is passed at 60 %, as in the exam.
"""

import re
from collections import defaultdict

from apps.accounts.levels import level_rank, visible_levels
from apps.exercises.models import Exercise

from . import grading
from .checks import MODUL_SIZE
from .learned import finished_units
from .models import ReadingResult, Unit

PASS_SHARE = 0.6
_SOURCE = re.compile(r"^seed-([a-c]\d)-lesen-m(\d+)-t(\d+)$")


class LesenNotFound(Exception):
    """No such set or Teil (or one above the user's level)."""


class LesenLocked(Exception):
    """The set's Lektionen aren't finished yet."""


def lesen_source(level: str, modul: int, teil: int) -> str:
    return f"seed-{level.lower()}-lesen-m{modul}-t{teil}"


def _parse(source: str):
    """(level, modul, teil) of a Lesen exercise's source, or None."""
    m = _SOURCE.match(source)
    return (m[1].upper(), int(m[2]), int(m[3])) if m else None


def _sets(levels) -> dict[tuple[str, int], list[tuple[int, Exercise]]]:
    """{(level, modul): [(teil, exercise), ...] in Teil order}."""
    out = defaultdict(list)
    for exercise in Exercise.objects.filter(source__contains="-lesen-m"):
        key = _parse(exercise.source)
        if key and key[0] in levels:
            out[key[:2]].append((key[2], exercise))
    for teile in out.values():
        teile.sort(key=lambda t: t[0])
    return out


def _lektionen(modul: int) -> range:
    return range((modul - 1) * MODUL_SIZE + 1, modul * MODUL_SIZE + 1)


def _is_open(user, level: str, modul: int, finished: set) -> bool:
    if level_rank(level) < level_rank(user.profile.cefr_level):
        return True
    return all((level, n) in finished for n in _lektionen(modul))


def _finished(user) -> set[tuple[str, int]]:
    """(level, Lektion) of every finished unit."""
    ids = finished_units(user)
    return set(Unit.objects.filter(id__in=ids).values_list("cefr_level", "order"))


def _score(teile, results) -> dict:
    """Questions, best right answers (once every Teil is done) and passed."""
    total = sum(len(grading.parts_of(e)) for _, e in teile)
    done = [results.get(e.id) for _, e in teile]
    if total and all(done):
        best = sum(r.best_correct for r in done)
        return {"questions": total, "best": best, "passed": best >= PASS_SHARE * total}
    return {"questions": total, "best": None, "passed": False}


def status(user) -> list[dict]:
    """Every set the user may see, lowest level first, with locks and best scores."""
    finished = _finished(user)
    results = {r.exercise_id: r for r in ReadingResult.objects.filter(user=user)}
    sets = _sets(visible_levels(user.profile.cefr_level))
    out = []
    for (level, modul), teile in sorted(
        sets.items(), key=lambda kv: (level_rank(kv[0][0]), kv[0][1])
    ):
        lektionen = _lektionen(modul)
        out.append(
            {
                "cefr_level": level,
                "modul": modul,
                "first": lektionen[0],
                "last": lektionen[-1],
                "locked": not _is_open(user, level, modul, finished),
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
        )
    return out


def _open_set(user, level: str, modul: int) -> list[tuple[int, Exercise]]:
    level = level.upper()
    if level not in visible_levels(user.profile.cefr_level):
        raise LesenNotFound("No such Lesen set.")
    teile = _sets([level]).get((level, modul))
    if not teile:
        raise LesenNotFound("No such Lesen set.")
    if not _is_open(user, level, modul, _finished(user)):
        raise LesenLocked("Finish this Modul's Lektionen first.")
    return teile


def detail(user, level: str, modul: int) -> dict:
    """One open set: its Teile without answers."""
    teile = _open_set(user, level, modul)
    results = {r.exercise_id: r for r in ReadingResult.objects.filter(user=user)}
    lektionen = _lektionen(modul)
    return {
        "cefr_level": level.upper(),
        "modul": modul,
        "first": lektionen[0],
        "last": lektionen[-1],
        "pass_share": PASS_SHARE,
        **_score(teile, results),
        "teile": [
            {
                "teil": teil,
                "best": results[e.id].best_correct if e.id in results else None,
                **grading.public_exercise(e),
            }
            for teil, e in teile
        ],
    }


def answer(user, exercise_id: int, given) -> dict:
    """Grade one Teil, keep the best result and reveal the solution."""
    exercise = Exercise.objects.filter(id=exercise_id, source__contains="-lesen-m").first()
    key = _parse(exercise.source) if exercise else None
    if key is None:
        raise LesenNotFound("No such Teil.")
    _open_set(user, key[0], key[1])

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
