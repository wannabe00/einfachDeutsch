"""Exam-style sets, one per Modul, shared by Lesen and Schreiben.

Each Teil of a set is a seeded exercise with the source
`seed-<level>-<skill>-m<modul>-t<teil>` (skill `lesen`, `schreiben` or `hoeren`), written
in `content/<level>/<skill>.py`. A set opens once its Modul's three Lektionen
are finished; every set of a level below the user's is open, and levels above
are never shown. Sets are passed at 60 %, as in the Goethe exams.
"""

import re
from collections import defaultdict

from apps.accounts.levels import level_rank, visible_levels
from apps.exercises.models import Exercise

from .checks import MODUL_SIZE
from .learned import finished_units
from .models import Unit

PASS_SHARE = 0.6
SKILLS = ("lesen", "schreiben", "hoeren")
_SOURCE = re.compile(r"^seed-([a-c]\d)-(lesen|schreiben|hoeren)-m(\d+)-t(\d+)$")


class SetNotFound(Exception):
    """No such set or Teil (or one above the user's level)."""


class SetLocked(Exception):
    """The set's Lektionen aren't finished yet."""


def set_source(skill: str, level: str, modul: int, teil: int) -> str:
    return f"seed-{level.lower()}-{skill}-m{modul}-t{teil}"


def parse_source(source: str):
    """(skill, level, modul, teil) of a set exercise's source, or None."""
    m = _SOURCE.match(source)
    return (m[2], m[1].upper(), int(m[3]), int(m[4])) if m else None


def sets_of(skill: str, levels) -> dict[tuple[str, int], list[tuple[int, Exercise]]]:
    """{(level, modul): [(teil, exercise), ...] in Teil order}, lowest level first."""
    out = defaultdict(list)
    for exercise in Exercise.objects.filter(source__contains=f"-{skill}-m"):
        key = parse_source(exercise.source)
        if key and key[0] == skill and key[1] in levels:
            out[(key[1], key[2])].append((key[3], exercise))
    for teile in out.values():
        teile.sort(key=lambda t: t[0])
    return dict(sorted(out.items(), key=lambda kv: (level_rank(kv[0][0]), kv[0][1])))


def lektionen(modul: int) -> range:
    return range((modul - 1) * MODUL_SIZE + 1, modul * MODUL_SIZE + 1)


def header(level: str, modul: int) -> dict:
    r = lektionen(modul)
    return {"cefr_level": level, "modul": modul, "first": r[0], "last": r[-1]}


def finished_lektionen(user) -> set[tuple[str, int]]:
    """(level, Lektion) of every finished unit."""
    ids = finished_units(user)
    return set(Unit.objects.filter(id__in=ids).values_list("cefr_level", "order"))


def is_open(user, level: str, modul: int, finished: set) -> bool:
    if level_rank(level) < level_rank(user.profile.cefr_level):
        return True
    return all((level, n) in finished for n in lektionen(modul))


def visible_sets(user, skill: str):
    """[(level, modul, teile, locked)] for every set the user may see."""
    finished = finished_lektionen(user)
    sets = sets_of(skill, visible_levels(user.profile.cefr_level))
    return [
        (level, modul, teile, not is_open(user, level, modul, finished))
        for (level, modul), teile in sets.items()
    ]


def open_set(user, skill: str, level: str, modul: int) -> list[tuple[int, Exercise]]:
    level = level.upper()
    if level not in visible_levels(user.profile.cefr_level):
        raise SetNotFound("No such set.")
    teile = sets_of(skill, [level]).get((level, modul))
    if not teile:
        raise SetNotFound("No such set.")
    if not is_open(user, level, modul, finished_lektionen(user)):
        raise SetLocked("Finish this Modul's Lektionen first.")
    return teile


def open_teil(user, skill: str, exercise_id: int) -> tuple[Exercise, tuple]:
    """A Teil of a set the user has open, with its parsed source."""
    exercise = Exercise.objects.filter(id=exercise_id, source__contains=f"-{skill}-m").first()
    key = parse_source(exercise.source) if exercise else None
    if key is None or key[0] != skill:
        raise SetNotFound("No such Teil.")
    open_set(user, skill, key[1], key[2])
    return exercise, key
