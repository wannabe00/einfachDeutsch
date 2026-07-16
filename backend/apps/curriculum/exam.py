"""Level checkpoint exam (Phase 23.14, Spec v3).

Finishing (at/near 100%) a level's path unlocks a Goethe-style exam: **pass →
promoted to the next level, fail → back to review** and retry.

Design notes:
  * Questions are **sampled from the level's own exercises** rather than authored
    separately. That keeps the exam automatically in sync as content grows
    (23.3b) instead of drifting, and needs no extra authoring.
  * Grading is deterministic/local, like the lesson player — free users must be
    gradable, and AI is premium.
  * The question set is **fixed when the attempt starts** and graded against on
    submit, so a client can't substitute easier questions.
  * Only unambiguously gradable types are sampled (no free_text, which needs AI).
"""

import random

from django.conf import settings
from django.utils import timezone

from apps.accounts.levels import LEVEL_RANK, level_rank, visible_levels
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
]


def next_level_of(level: str) -> str | None:
    """The level after `level`, or None at the top of the ladder."""
    ordered = sorted(LEVEL_RANK, key=LEVEL_RANK.get)
    idx = level_rank(level)
    return ordered[idx + 1] if idx + 1 < len(ordered) else None


def _level_exercise_qs(level: str):
    """Every gradable exercise taught anywhere in `level`'s path."""
    return Exercise.objects.filter(
        lesson_items__lesson__unit__cefr_level=level,
        exercise_type__in=GRADABLE_TYPES,
    ).distinct()


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
    pool = _level_exercise_qs(level).count()

    last = LevelExamAttempt.objects.filter(
        user=user, cefr_level=level, completed_at__isnull=False
    ).first()

    return {
        "level": level,
        "next_level": next_level_of(level),
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
    ids = list(_level_exercise_qs(level).values_list("id", flat=True))
    picked = random.sample(ids, min(QUESTION_COUNT, len(ids)))

    attempt = LevelExamAttempt.objects.create(user=user, cefr_level=level, question_ids=picked)
    # Preserve the sampled order rather than the DB's.
    by_id = {e.id: e for e in Exercise.objects.filter(id__in=picked)}
    questions = [grading.public_exercise(by_id[i]) for i in picked if i in by_id]
    return attempt, questions


def submit_attempt(user, attempt_id: int, answers: dict) -> dict:
    """Grade a frozen attempt, promote on a pass, and report the outcome.

    `answers` maps exercise_id → answer. Anything not in the attempt's frozen
    question set is ignored; missing answers simply score zero.
    """
    attempt = LevelExamAttempt.objects.filter(user=user, pk=attempt_id).first()
    if attempt is None:
        raise ExamError("Exam attempt not found.")
    if attempt.completed_at:
        raise ExamError("This attempt has already been submitted.")

    exercises = {e.id: e for e in Exercise.objects.filter(id__in=attempt.question_ids)}
    total = len(attempt.question_ids) or 1
    correct = sum(
        1
        for qid in attempt.question_ids
        if qid in exercises
        and grading.grade(exercises[qid], answers.get(str(qid), answers.get(qid)))
    )
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
        "level": user.profile.cefr_level,
        "visible_levels": visible_levels(user.profile.cefr_level),
    }
