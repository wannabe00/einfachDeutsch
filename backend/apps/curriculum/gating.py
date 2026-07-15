"""Level- and progression-gating helpers (Spec v3).

Rules:
- A user sees content **≤ their level**. Below their level = optional review
  (fully unlocked); their current level = strictly linear; above = locked.
- Within the current level the path is linear: a lesson is unlocked once the
  immediately-preceding lesson in the level is completed.

Pure-ish functions used by serializers/views in later bricks (23.4, 23.8).
"""

from apps.accounts.models import CEFR_LEVELS

from .models import Lesson, PathLessonProgress

# A1=0, A2=1, … C2=5 — CEFR codes also sort lexicographically, but rank by this.
LEVEL_RANK = {code: i for i, (code, _) in enumerate(CEFR_LEVELS)}


def level_rank(code: str) -> int:
    return LEVEL_RANK.get(code, 0)


def visible_levels(user_level: str) -> list[str]:
    """Every level at or below the user's, in order (what they may browse)."""
    ceiling = level_rank(user_level)
    return [code for code, _ in CEFR_LEVELS if level_rank(code) <= ceiling]


def is_level_visible(user_level: str, content_level: str) -> bool:
    return level_rank(content_level) <= level_rank(user_level)


def _level_lesson_ids(level: str) -> list[int]:
    """Lesson ids for a level in path order (unit order, then lesson order)."""
    return list(
        Lesson.objects.filter(unit__cefr_level=level)
        .order_by("unit__order", "order")
        .values_list("id", flat=True)
    )


def path_states(user, units) -> tuple[dict[int, str], Lesson | None]:
    """Bulk state for a whole path render — the same rules as `is_lesson_unlocked`,
    but in one pass (that helper is per-lesson and would be N queries here).

    Returns ({lesson_id: "completed"|"current"|"available"|"locked"}, next_lesson).
    `next_lesson` (and the single "current" state) is the first open, incomplete
    lesson **at the user's own level** — lessons below their level are optional
    review, so they never claim "current".

    `units` must be prefetched with their lessons.
    """
    user_level = user.profile.cefr_level
    completed = set(
        PathLessonProgress.objects.filter(user=user, completed_at__isnull=False).values_list(
            "lesson_id", flat=True
        )
    )

    by_level: dict[str, list[tuple[int, int, Lesson]]] = {}
    for unit in units:
        for lesson in unit.lessons.all():
            by_level.setdefault(unit.cefr_level, []).append((unit.order, lesson.order, lesson))

    states: dict[int, str] = {}
    next_lesson: Lesson | None = None

    for level, rows in by_level.items():
        rows.sort(key=lambda r: (r[0], r[1]))
        is_review = level_rank(level) < level_rank(user_level)
        # Sentinel: the first lesson of a level is always unlocked.
        prev_completed = True
        for _, _, lesson in rows:
            if lesson.id in completed:
                states[lesson.id] = "completed"
                prev_completed = True
                continue
            unlocked = is_review or prev_completed
            if not unlocked:
                states[lesson.id] = "locked"
            elif level == user_level and next_lesson is None:
                states[lesson.id] = "current"
                next_lesson = lesson
            else:
                states[lesson.id] = "available"
            prev_completed = False

    return states, next_lesson


def is_lesson_unlocked(user, lesson: Lesson) -> bool:
    """Whether `user` may start `lesson` given their level + linear progress."""
    user_level = user.profile.cefr_level
    lesson_level = lesson.unit.cefr_level

    if level_rank(lesson_level) < level_rank(user_level):
        return True  # below current level → review, always open
    if level_rank(lesson_level) > level_rank(user_level):
        return False  # above current level → locked

    # Current level: linear. Unlocked if first in the level, or the previous
    # lesson is completed.
    ids = _level_lesson_ids(lesson_level)
    try:
        idx = ids.index(lesson.id)
    except ValueError:
        return False
    if idx == 0:
        return True
    return PathLessonProgress.objects.filter(
        user=user, lesson_id=ids[idx - 1], completed_at__isnull=False
    ).exists()
