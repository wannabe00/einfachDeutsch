"""What a user has learned.

One answer, used by every page that should only show material the user has
reached (Word Bank, Grammar, Review, Exercises, Drills, Books):

  - a word is learned once the user completes the lesson that teaches it
    (`Lesson.words`); a grammar topic once they complete a lesson that shows
    its explanation card
  - everything from levels below the user's own counts as learned: they were
    placed or promoted past it
  - content no path lesson teaches (older chapters, words a user added) has
    nothing to wait for, so it counts as learned
  - nothing above the user's level is ever learned

Guests have no progress, so for them nothing on the path is learned.
"""

from apps.accounts.levels import level_rank
from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word

from .models import Lesson, LessonItem, PathLessonProgress, Unit


def completed_lesson_ids(user) -> set[int]:
    if user is None or not user.is_authenticated:
        return set()
    return set(
        PathLessonProgress.objects.filter(user=user, completed_at__isnull=False).values_list(
            "lesson_id", flat=True
        )
    )


def _learned_ids(user, model, taught: dict[int, set[int]]) -> set[int]:
    """Ids of `model` rows learned by `user`, given {row_id: teaching lesson ids}."""
    if user is None or not user.is_authenticated:
        return set()
    done = completed_lesson_ids(user)
    rank = level_rank(user.profile.cefr_level)
    learned = set()
    for row_id, level in model.objects.values_list("id", "chapter__cefr_level"):
        if level_rank(level) > rank:
            continue
        lessons = taught.get(row_id)
        if lessons is None or level_rank(level) < rank or lessons & done:
            learned.add(row_id)
    return learned


def learned_word_ids(user) -> set[int]:
    taught: dict[int, set[int]] = {}
    for lesson_id, word_id in Lesson.words.through.objects.values_list("lesson_id", "word_id"):
        taught.setdefault(word_id, set()).add(lesson_id)
    return _learned_ids(user, Word, taught)


def learned_rule_ids(user) -> set[int]:
    taught: dict[int, set[int]] = {}
    items = LessonItem.objects.filter(grammar_rule__isnull=False)
    for lesson_id, rule_id in items.values_list("lesson_id", "grammar_rule_id"):
        taught.setdefault(rule_id, set()).add(lesson_id)
    return _learned_ids(user, GrammarRule, taught)


def teaching_lessons(rule_ids) -> dict[int, Lesson]:
    """{rule_id: the first lesson on the path that teaches it}."""
    items = (
        LessonItem.objects.filter(grammar_rule_id__in=rule_ids)
        .select_related("lesson__unit")
        .order_by("lesson__unit__cefr_level", "lesson__unit__order", "lesson__order")
    )
    out: dict[int, Lesson] = {}
    for item in items:
        out.setdefault(item.grammar_rule_id, item.lesson)
    return out


def last_completed_unit(user) -> Unit | None:
    """The unit the user finished most recently (every lesson completed), for
    the Dashboard's "review last unit". None until a whole unit is done."""
    if user is None or not user.is_authenticated:
        return None
    finished_at: dict[int, object] = {}
    done_count: dict[int, int] = {}
    rows = PathLessonProgress.objects.filter(user=user, completed_at__isnull=False).values_list(
        "lesson__unit_id", "completed_at"
    )
    for unit_id, completed_at in rows:
        done_count[unit_id] = done_count.get(unit_id, 0) + 1
        finished_at[unit_id] = max(finished_at.get(unit_id, completed_at), completed_at)

    rank = level_rank(user.profile.cefr_level)
    units = Unit.objects.filter(id__in=done_count).prefetch_related("lessons")
    finished = [
        u
        for u in units
        if done_count[u.id] >= len(u.lessons.all()) and level_rank(u.cefr_level) <= rank
    ]
    return max(finished, key=lambda u: finished_at[u.id], default=None)
