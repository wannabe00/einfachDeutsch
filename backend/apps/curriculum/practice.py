"""Practice sets: short, slightly harder practice from finished lessons.

A set is about ten tasks drawn from the exercises of lessons the user has
completed, mixed across units. It's meant to be a bit harder than the lessons:

  * no hints
  * typing and word order are picked more often than multiple choice, and
    matching is left out (it's recognition, not recall)
  * a big multi-part exercise is cut down to a few of its parts
  * exercises answered wrongly in the last weeks come back more often

A task is referred to as "12" (exercise 12) or "12:0,3,5" (those parts of
multi-part exercise 12), so it can be graded without storing the set.
"""

import random
from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone

from apps.exercises.models import ExerciseAttempt
from apps.grammar.models import GrammarRule

from . import grading
from .models import LessonItem, PathLessonProgress

SET_SIZE = 10
MAX_PARTS_PER_TASK = 4
# How often each type is picked, relative to the others.
TYPE_WEIGHT = {
    "translation": 3,
    "fill_blank": 3,
    "conjugation": 3,
    "article": 2,
    "sentence_order": 3,
    "word_bank": 2,
    "multiple_choice": 1,
}
# Each recent wrong answer makes an exercise this much more likely.
WRONG_BOOST = 2
WRONG_WINDOW_DAYS = 30


class PracticeError(Exception):
    """A task that isn't the user's to practise (or doesn't exist)."""


def _practice_items(user):
    """(item, unit, topic_rule_id) for every exercise in a completed lesson.

    The topic is the grammar explanation shown before the exercise in its
    lesson (None for vocabulary practice before any explanation).
    """
    done = PathLessonProgress.objects.filter(user=user, completed_at__isnull=False).values(
        "lesson_id"
    )
    items = (
        LessonItem.objects.filter(lesson_id__in=done)
        .select_related("exercise", "lesson__unit")
        .order_by("lesson_id", "order")
    )
    out, topic, lesson_id = [], None, None
    for item in items:
        if item.lesson_id != lesson_id:
            topic, lesson_id = None, item.lesson_id
        if item.grammar_rule_id:
            topic = item.grammar_rule_id
        elif item.exercise_id:
            out.append((item, item.lesson.unit, topic))
    return out


def _practisable_parts(exercise) -> list[int]:
    """Indexes of the parts worth practising (matching is left out)."""
    return [i for i, p in enumerate(grading.parts_of(exercise)) if p.get("type") in TYPE_WEIGHT]


def options(user) -> dict:
    """The units and grammar topics a set can be narrowed to."""
    units, topics = {}, {}
    for item, unit, topic in _practice_items(user):
        if not _practisable_parts(item.exercise):
            continue
        units[unit.id] = {"id": unit.id, "order": unit.order, "title": unit.title}
        if topic:
            topics[topic] = None
    rules = GrammarRule.objects.filter(id__in=topics).order_by("chapter__number", "id")
    return {
        "units": sorted(units.values(), key=lambda u: u["order"]),
        "topics": [{"id": r.id, "title": r.title} for r in rules],
    }


def _recent_wrong(user) -> dict[int, int]:
    since = timezone.now() - timedelta(days=WRONG_WINDOW_DAYS)
    rows = (
        ExerciseAttempt.objects.filter(user=user, attempted_at__gte=since)
        .values("exercise_id")
        .annotate(wrong=Count("id", filter=Q(is_correct=False)))
    )
    return {r["exercise_id"]: r["wrong"] for r in rows}


def _weighted_sample(candidates: list, weights: list[float], k: int) -> list:
    """Pick up to `k` distinct candidates, each with probability by weight."""
    pool = list(zip(candidates, weights, strict=True))
    picked = []
    while pool and len(picked) < k:
        total = sum(w for _, w in pool)
        r = random.uniform(0, total)
        for i, (cand, w) in enumerate(pool):
            r -= w
            if r <= 0:
                picked.append(cand)
                pool.pop(i)
                break
        else:
            picked.append(pool.pop()[0])
    return picked


def build_set(user, unit_id=None, topic_id=None) -> list[dict]:
    """A new practice set: up to SET_SIZE tasks, each stripped of hints and answers."""
    wrong = _recent_wrong(user)
    candidates, weights, seen = [], [], set()
    for item, unit, topic in _practice_items(user):
        ex = item.exercise
        if ex.id in seen or (unit_id and unit.id != unit_id) or (topic_id and topic != topic_id):
            continue
        parts = _practisable_parts(ex)
        if not parts:
            continue
        seen.add(ex.id)
        ptype = grading.parts_of(ex)[parts[0]]["type"]
        candidates.append((ex, parts))
        weights.append(TYPE_WEIGHT[ptype] * (1 + WRONG_BOOST * wrong.get(ex.id, 0)))

    tasks = []
    for ex, parts in _weighted_sample(candidates, weights, SET_SIZE):
        if ex.exercise_type == "group":
            chosen = sorted(random.sample(parts, min(MAX_PARTS_PER_TASK, len(parts))))
            tasks.append(_public_task(ex, chosen))
        else:
            tasks.append(_public_task(ex, None))
    return tasks


def _public_task(exercise, part_indexes) -> dict:
    """A task as the client sees it: no answers, no hints."""
    if part_indexes is None:
        task = grading.public_part(grading.parts_of(exercise)[0])
        task_id = str(exercise.id)
    else:
        all_parts = grading.parts_of(exercise)
        parts = [{**grading.public_part(all_parts[i]), "hint": ""} for i in part_indexes]
        task = {"type": "group", "prompt": exercise.prompt, "payload": {"parts": parts}}
        task_id = f"{exercise.id}:{','.join(map(str, part_indexes))}"
        if len(parts) == 1:
            task = {**parts[0], "prompt": parts[0]["prompt"] or exercise.prompt}
    return {**task, "hint": "", "task_id": task_id}


def answer(user, task_id: str, given) -> dict:
    """Grade one task, record the attempt, and reveal the solution."""
    ex_id, _, indexes = str(task_id).partition(":")
    try:
        ex_id = int(ex_id)
        part_indexes = [int(i) for i in indexes.split(",")] if indexes else None
    except ValueError as err:
        raise PracticeError("Unknown task.") from err

    item = next((i for i, _, _ in _practice_items(user) if i.exercise_id == ex_id), None)
    if item is None:
        raise PracticeError("Practice only covers lessons you've finished.")
    exercise = item.exercise
    all_parts = grading.parts_of(exercise)
    if part_indexes is None:
        parts = all_parts[:1]
    elif all(0 <= i < len(all_parts) for i in part_indexes):
        parts = [all_parts[i] for i in part_indexes]
    else:
        raise PracticeError("Unknown task.")

    # One part is answered with a plain value, several with a list.
    answers = [given] if len(parts) == 1 else (given if isinstance(given, list) else [])
    verdicts = [
        grading.grade_part(p, answers[i] if i < len(answers) else None) for i, p in enumerate(parts)
    ]
    ExerciseAttempt.objects.create(
        user=user, exercise=exercise, user_answer=str(given), is_correct=all(verdicts)
    )
    solutions = [grading.solution_of_part(p) for p in parts]
    return {
        "correct": all(verdicts),
        "parts": verdicts,
        "solution": solutions[0] if len(parts) == 1 else solutions,
        "explanation": exercise.explanation,
    }
