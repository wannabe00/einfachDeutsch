"""Level checkpoint exam.

Finishing (almost) all of a level's path unlocks an exam. Pass and you move up
a level; fail and you go back to review and can retry.

Notes:
  * Questions are sampled from the level's own exercises instead of being
    written separately, so the exam keeps up as content is added.
  * Grading is local, like the lesson player, because free users need grading
    and AI is premium.
  * The question set is stored when the attempt starts and graded against on
    submit, so a client can't swap in easier questions.
  * Only types with one clear answer are sampled (no free_text, which needs AI).
  * A multi-part exercise isn't asked whole: each of its parts is a question
    of its own, so every question is one screen and weighs the same. A
    question is referred to as "12" (an exercise) or "12:3" (part 3 of
    exercise 12).
"""

import random

from django.conf import settings
from django.utils import timezone

from apps.accounts.levels import COURSE_LEVELS, TOP_LEVEL, visible_levels
from apps.exercises.models import Exercise

from . import grading
from .models import Lesson, LevelExamAttempt, PathLessonProgress

UNLOCK_RATIO = getattr(settings, "EXAM_UNLOCK_RATIO", 0.9)
PASS_THRESHOLD = getattr(settings, "EXAM_PASS_THRESHOLD", 0.8)
QUESTION_COUNT = getattr(settings, "EXAM_QUESTION_COUNT", 12)


class ExamError(Exception):
    """A rule the exam enforces (locked, already submitted, missing)."""


GRADABLE_TYPES = [
    "multiple_choice",
    "translation",
    "fill_blank",
    "article",
    "conjugation",
    "sentence_order",
    "word_bank",
    "matching",
    "group",
]


def next_level_of(level: str) -> str | None:
    """The level after `level`, or None at the top of the course (B1)."""
    idx = COURSE_LEVELS.index(level) if level in COURSE_LEVELS else len(COURSE_LEVELS)
    return COURSE_LEVELS[idx + 1] if idx + 1 < len(COURSE_LEVELS) else None


def course_complete(user) -> bool:
    """Passed the exam of the course's last level: the whole course is done."""
    return LevelExamAttempt.objects.filter(user=user, cefr_level=TOP_LEVEL, passed=True).exists()


def _level_exercise_qs(level: str):
    """Every gradable exercise taught anywhere in `level`'s path."""
    return Exercise.objects.filter(
        lesson_items__lesson__unit__cefr_level=level,
        exercise_type__in=GRADABLE_TYPES,
    ).distinct()


def _question_refs(level: str) -> list[str]:
    """Every question the exam can ask at `level`: whole exercises and the
    parts of multi-part ones."""
    qs = _level_exercise_qs(level)
    refs = [str(i) for i in qs.exclude(exercise_type="group").values_list("id", flat=True)]
    for ex in qs.filter(exercise_type="group"):
        refs += [f"{ex.id}:{i}" for i in range(len(grading.parts_of(ex)))]
    return refs


def _resolve(ref, exercises: dict) -> dict | None:
    """The part a question ref points at, or None if it no longer exists."""
    ex_id, _, index = str(ref).partition(":")
    ex = exercises.get(int(ex_id))
    if ex is None:
        return None
    parts = grading.parts_of(ex)
    i = int(index or 0)
    return parts[i] if i < len(parts) else None


def _exercises_for(refs) -> dict:
    ids = {int(str(r).partition(":")[0]) for r in refs}
    return {e.id: e for e in Exercise.objects.filter(id__in=ids)}


def exam_status(user) -> dict:
    """What the path page needs: progress toward the exam, and whether it's open."""
    level = user.profile.cefr_level
    total = Lesson.objects.filter(unit__cefr_level=level).count()
    completed = (
        PathLessonProgress.objects.filter(
            user=user, lesson__unit__cefr_level=level, completed_at__isnull=False
        )
        .values("lesson_id")
        .distinct()
        .count()
    )
    ratio = (completed / total) if total else 0.0
    pool = len(_question_refs(level))

    last = LevelExamAttempt.objects.filter(
        user=user, cefr_level=level, completed_at__isnull=False
    ).first()

    return {
        "level": level,
        "next_level": next_level_of(level),
        "course_complete": course_complete(user),
        "completed_lessons": completed,
        "total_lessons": total,
        "progress": round(ratio, 3),
        "unlock_ratio": UNLOCK_RATIO,
        # No path (or no questions) → nothing to examine.
        "unlocked": bool(total) and ratio >= UNLOCK_RATIO and pool > 0,
        "pass_threshold": PASS_THRESHOLD,
        "question_count": min(QUESTION_COUNT, pool),
        "last_attempt": (
            {
                "score": last.score,
                "passed": last.passed,
                "completed_at": last.completed_at,
            }
            if last
            else None
        ),
    }


def start_attempt(user) -> tuple[LevelExamAttempt, list[dict]]:
    """Open an attempt: sample the questions, freeze them, return them stripped."""
    status = exam_status(user)
    if not status["unlocked"]:
        raise ExamError("Finish your level's path first.")

    level = user.profile.cefr_level
    refs = _question_refs(level)
    picked = random.sample(refs, min(QUESTION_COUNT, len(refs)))

    attempt = LevelExamAttempt.objects.create(user=user, cefr_level=level, question_ids=picked)
    exercises = _exercises_for(picked)
    questions = [
        {"question_id": ref, **grading.public_part(_resolve(ref, exercises))} for ref in picked
    ]
    return attempt, questions


def submit_attempt(user, attempt_id: int, answers: dict) -> dict:
    """Grade a frozen attempt, promote on a pass, and report the outcome.

    `answers` maps question_id → answer. Anything not in the attempt's frozen
    question set is ignored; missing answers simply score zero.
    """
    attempt = LevelExamAttempt.objects.filter(user=user, pk=attempt_id).first()
    if attempt is None:
        raise ExamError("Exam attempt not found.")
    if attempt.completed_at:
        raise ExamError("This attempt has already been submitted.")

    exercises = _exercises_for(attempt.question_ids)
    total = len(attempt.question_ids) or 1
    correct = 0
    for ref in attempt.question_ids:
        part = _resolve(ref, exercises)
        if part is not None and grading.grade_part(part, answers.get(str(ref))):
            correct += 1
    score = correct / total
    passed = score >= PASS_THRESHOLD

    attempt.score = score
    attempt.passed = passed
    attempt.completed_at = timezone.now()
    attempt.save(update_fields=["score", "passed", "completed_at"])

    promoted_to = None
    if passed:
        nxt = next_level_of(attempt.cefr_level)
        # Only ever move forward, and only from the level actually examined.
        if nxt and user.profile.cefr_level == attempt.cefr_level:
            user.profile.cefr_level = nxt
            user.profile.save(update_fields=["cefr_level"])
            promoted_to = nxt

    return {
        "passed": passed,
        "score": round(score, 3),
        "correct": correct,
        "total": total,
        "pass_threshold": PASS_THRESHOLD,
        "promoted_to": promoted_to,
        "course_complete": passed and attempt.cefr_level == TOP_LEVEL,
        "level": user.profile.cefr_level,
        "visible_levels": visible_levels(user.profile.cefr_level),
    }
