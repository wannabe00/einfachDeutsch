"""The learning path.

Shared content (Unit, Lesson, LessonItem) plus per-user progress
(PathLessonProgress, LessonDraft) and energy (EnergyState). As elsewhere in the project,
content has no per-user foreign keys.

A book Lektion is a Unit here, not a Lesson. Each Lektion is played as 2-3
Lessons (Wortschatz, Grammatik, Kommunikation und Wiederholung).
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
    # One Lektion is one Unit and one Chapter. The chapter holds the unit's full
    # word list and grammar so the unit page can show them for review. Nullable
    # because a unit can exist before its content is seeded.
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
    """One lesson on the path: 20-30 minutes of cards and grouped exercises."""

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lessons")
    order = models.PositiveIntegerField(default=0)  # position within the unit
    title = models.CharField(max_length=200)
    xp_reward = models.PositiveIntegerField(default=10)
    # The words this lesson introduces. Finishing the lesson marks them learned
    # (see curriculum.learned). Each of a unit's words is taught by one lesson.
    words = models.ManyToManyField("vocabulary.Word", blank=True, related_name="taught_in")

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


class LessonDraft(models.Model):
    """A lesson the user has started but not finished: the answers checked so
    far and where to pick up. Removed when the lesson is finished."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_drafts"
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="drafts")
    # {item_id (as a string, it's JSON): answer}
    answers = models.JSONField(default=dict)
    step = models.PositiveIntegerField(default=0)  # index of the next item to show
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("user", "lesson")]

    def __str__(self):
        return f"{self.user} … {self.lesson} (step {self.step})"


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


class LevelExamAttempt(models.Model):
    """A Goethe-style checkpoint attempt.

    Unlocked once the user has essentially finished their level's path; passing
    promotes them to the next level, failing sends them back to review and they
    may retry.

    `question_ids` is fixed when the attempt starts and graded against on submit,
    so the client can't swap in easier questions.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exam_attempts"
    )
    cefr_level = models.CharField(max_length=2, choices=CEFR_LEVELS)
    question_ids = models.JSONField(default=list)
    score = models.FloatField(null=True, blank=True)  # 0..1, null until submitted
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at", "-id"]

    def __str__(self):
        state = "passed" if self.passed else ("failed" if self.completed_at else "in progress")
        return f"{self.user} · {self.cefr_level} exam ({state})"


class Check(models.Model):
    """A review or test of what a user has learned (see apps.curriculum.checks).

    * review: one finished Lektion, at the start of the next one or from the
      Dashboard: a third of its words in batches of five, plus a gap task and a
      translation task.
    * modul: after every three Lektionen, a longer mixed test across everything
      learned so far, scored per skill.

    The tasks are picked once, when the check starts, and kept here with the
    answers given so far, so a check can be left and resumed and only its own
    tasks can be answered. Checks never cost energy.
    """

    class Kind(models.TextChoices):
        REVIEW = "review", "Review"
        MODUL = "modul", "Modul test"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="checks"
    )
    kind = models.CharField(max_length=10, choices=Kind.choices)
    cefr_level = models.CharField(max_length=2, choices=CEFR_LEVELS)
    # review: the Lektion reviewed. modul: the Modul's last Lektion.
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="checks")
    modul = models.PositiveIntegerField(null=True, blank=True)
    # [{"id": task id, "skill": "words" | "grammar" | "listening" | "reading"}]
    tasks = models.JSONField(default=list)
    # {task id: {"correct", "parts", "solution", "explanation"}}
    results = models.JSONField(default=dict)
    score = models.FloatField(null=True, blank=True)  # 0..1, set when finished
    # {skill: [right parts, all parts]}
    skills = models.JSONField(default=dict)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at", "-id"]

    def __str__(self):
        what = f"Modul {self.modul}" if self.kind == self.Kind.MODUL else f"L{self.unit.order}"
        return f"{self.user} · {self.cefr_level} {what} ({self.kind})"


class ReadingResult(models.Model):
    """A user's result on one Teil of a Lesen set (see apps.curriculum.lesen).
    The Teil is a seeded exercise; the best score is kept for the set page."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reading_results"
    )
    exercise = models.ForeignKey(
        "exercises.Exercise", on_delete=models.CASCADE, related_name="reading_results"
    )
    correct = models.PositiveIntegerField(default=0)  # last attempt
    best_correct = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "exercise"], name="unique_reading_result")
        ]

    def __str__(self):
        return f"{self.user} · {self.exercise.source} {self.best_correct}/{self.total}"


class WritingAttempt(models.Model):
    """One try at a Schreiben Teil (see apps.curriculum.schreiben), kept with its
    text, score and feedback so the user can read past attempts again."""

    class GradedBy(models.TextChoices):
        AUTO = "auto", "Checked automatically"  # the form, or a text far too short
        SELF = "self", "Self-check"
        AI = "ai", "AI"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="writing_attempts"
    )
    exercise = models.ForeignKey(
        "exercises.Exercise", on_delete=models.CASCADE, related_name="writing_attempts"
    )
    answer = models.JSONField(default=str)  # the text, or the form's answers
    words = models.PositiveIntegerField(default=0)
    # Per content point: "full" | "partial" | "missing".
    points = models.JSONField(default=list, blank=True)
    score = models.FloatField(null=True, blank=True)  # null until graded
    max_score = models.FloatField(default=0)
    graded_by = models.CharField(max_length=4, choices=GradedBy.choices, blank=True)
    # Checks, grades per criterion, and the AI's corrected text and tips.
    feedback = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.user} · {self.exercise.source} {self.score}/{self.max_score}"
