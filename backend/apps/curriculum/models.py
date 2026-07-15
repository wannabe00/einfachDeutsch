"""Phase 23 — Learning Path data model.

Shared/global CONTENT (Unit → Lesson → LessonItem) plus per-user PROGRESS
(PathLessonProgress) and ENERGY (EnergyState). Follows the project's content-vs-
progress split: content carries no per-user FKs; progress/energy are per-user.

A book "Lektion" is *not* a Lesson here — the seed pipeline (23.3) slices book
structure into small ~6-item Lessons grouped under thematic Units. This model is
deliberately content-agnostic so that mapping can evolve.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.accounts.models import CEFR_LEVELS


class Unit(models.Model):
    """A themed section of a level's path (e.g. A1 · "Kennenlernen"). Contains
    an ordered list of Lessons. Global/shared content."""

    cefr_level = models.CharField(max_length=2, choices=CEFR_LEVELS)
    order = models.PositiveIntegerField(default=0)  # position within the level
    title = models.CharField(max_length=200)
    theme = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    # One Lektion = one Unit = one Chapter (Spec v3 mapping). The chapter is the
    # content container holding this unit's full Wortschatz / grammar, so the
    # unit page can show them for review. Nullable: units may exist before their
    # content is seeded.
    chapter = models.ForeignKey(
        "books.Chapter", null=True, blank=True, on_delete=models.SET_NULL, related_name="units"
    )
    # Per-unit accent for the Duolingo-style colourful sections (token name or
    # hex). Blank falls back to the global brand accent.
    accent_color = models.CharField(max_length=32, blank=True)

    class Meta:
        ordering = ["cefr_level", "order"]
        constraints = [
            models.UniqueConstraint(
                fields=["cefr_level", "order"], name="unique_unit_order_per_level"
            )
        ]

    def __str__(self):
        return f"{self.cefr_level} · U{self.order} {self.title}"


class Lesson(models.Model):
    """One "day"/lesson on the path — a small bundle of ~6 mixed items."""

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lessons")
    order = models.PositiveIntegerField(default=0)  # position within the unit
    title = models.CharField(max_length=200)
    xp_reward = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ["unit", "order"]
        constraints = [
            models.UniqueConstraint(fields=["unit", "order"], name="unique_lesson_order_per_unit")
        ]

    def __str__(self):
        return f"{self.unit.cefr_level} · {self.title}"


class LessonItem(models.Model):
    """One step inside a Lesson. `kind` selects which content FK is used, so a
    lesson can interleave exercises, drills, review cards, and grammar."""

    class Kind(models.TextChoices):
        EXERCISE = "exercise", "Exercise"
        DRILL = "drill", "Drill"
        REVIEW = "review", "Review"
        GRAMMAR = "grammar", "Grammar"

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="items")
    order = models.PositiveIntegerField(default=0)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.EXERCISE)
    # Exactly one of these is set, per `kind` (exercise/drill → exercise,
    # review → word, grammar → grammar_rule). Kept as explicit nullable FKs
    # rather than a generic relation for clarity + admin friendliness.
    exercise = models.ForeignKey(
        "exercises.Exercise",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="lesson_items",
    )
    word = models.ForeignKey(
        "vocabulary.Word",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="lesson_items",
    )
    grammar_rule = models.ForeignKey(
        "grammar.GrammarRule",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="lesson_items",
    )

    class Meta:
        ordering = ["lesson", "order"]

    def __str__(self):
        return f"{self.lesson} · #{self.order} ({self.kind})"


class PathLessonProgress(models.Model):
    """Per-user completion of a path Lesson. One row per (user, lesson)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="path_progress"
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="completions")
    completed_at = models.DateTimeField(null=True, blank=True)
    best_score = models.FloatField(null=True, blank=True)  # 0..1
    crown = models.PositiveIntegerField(default=0)  # crown level earned
    xp_earned = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [("user", "lesson")]

    @property
    def is_complete(self):
        return self.completed_at is not None

    def __str__(self):
        state = "✓" if self.is_complete else "…"
        return f"{self.user} {state} {self.lesson}"


class EnergyState(models.Model):
    """Per-user energy for the free tier. `balance` is the value as of
    `last_refill_at`; the live value is derived by adding time-based regen
    (see apps.curriculum.energy). Premium users bypass energy entirely."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="energy"
    )
    balance = models.PositiveIntegerField(default=3)
    last_refill_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}: {self.balance}⚡ @ {self.last_refill_at:%Y-%m-%d %H:%M}"
