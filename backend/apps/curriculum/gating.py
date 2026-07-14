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
