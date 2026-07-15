"""Grammar unlocking (Phase 23.10).

Spec v3: a grammar topic unlocks with **the lesson that teaches it** — grammar
lives on only some Lektionen, so topics are tied to specific lessons rather than
to progress in general.

Rules:
  - a topic **below** the user's level is optional review → always open
  - a topic at the user's level that a lesson teaches → locked until that lesson
    is completed
  - a topic **no lesson references** (legacy content) can't be locked by this
    rule, so it stays open — otherwise the existing library would vanish

(Topics *above* the user's level never appear at all; the ≤-level filter from
23.8 drops them before this runs.)
"""

from apps.accounts.levels import level_rank


def grammar_unlock_map(user) -> dict[int, dict]:
    """`{rule_id: {"locked": bool, "lesson": {...} | None}}` for every grammar
    rule a lesson teaches. Rules absent from the map are unlocked."""
    if user is None or not getattr(user, "is_authenticated", False):
        return {}

    # Imported lazily so `grammar` keeps no hard dependency on `curriculum`.
    from apps.curriculum.models import LessonItem, PathLessonProgress

    user_rank = level_rank(user.profile.cefr_level)
    completed = set(
        PathLessonProgress.objects.filter(user=user, completed_at__isnull=False).values_list(
            "lesson_id", flat=True
        )
    )

    out: dict[int, dict] = {}
    items = (
        LessonItem.objects.filter(grammar_rule__isnull=False)
        .select_related("lesson__unit", "grammar_rule__chapter")
        .order_by("lesson__unit__order", "lesson__order")
    )
    for item in items:
        rule = item.grammar_rule
        lesson = item.lesson
        unit = lesson.unit

        # Below the user's level → review, always open.
        is_review = level_rank(rule.chapter.cefr_level) < user_rank
        unlocked = is_review or lesson.id in completed

        entry = out.get(rule.id)
        if entry is None:
            out[rule.id] = {
                "locked": not unlocked,
                "lesson": {
                    "id": lesson.id,
                    "title": lesson.title,
                    "unit_id": unit.id,
                    "unit_title": unit.title,
                    "unit_order": unit.order,
                    "lesson_order": lesson.order,
                },
            }
        elif unlocked:
            # Taught by several lessons: finishing any one of them unlocks it.
            entry["locked"] = False

    return out
