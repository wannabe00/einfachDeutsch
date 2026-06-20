from django.conf import settings
from django.db import models

CEFR_LEVELS = [
    ("A1", "A1"),
    ("A2", "A2"),
    ("B1", "B1"),
    ("B2", "B2"),
    ("C1", "C1"),
    ("C2", "C2"),
]

ROLE_CHOICES = [
    ("student", "Student"),
    ("teacher", "Teacher"),
]


class UserProfile(models.Model):
    """Per-user account state. One row per auth User.

    `role` is forward-compat for teachers: content is already shared and
    progress is per-user, so a future Teacher↔Student link model (+ per-student
    curation) can be layered on without reshaping existing tables. Everyone is a
    `student` until promoted.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    cefr_level = models.CharField(max_length=2, choices=CEFR_LEVELS, default="A1")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")
    # Set once the user has chosen/confirmed their level (onboarding). Until
    # then the frontend shows the level picker / placement test.
    level_set = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} ({self.cefr_level})"


class LevelDefinition(models.Model):
    """Completion thresholds for one CEFR level (Phase 14).

    A user advances out of their current level once they've completed
    `required_lessons` lessons and done `required_reviews` reviews. Numbers are
    editable in the admin (tunable, not hardcoded).
    """

    cefr_level = models.CharField(max_length=2, choices=CEFR_LEVELS, unique=True)
    order = models.PositiveIntegerField(default=0)  # A1=1 … C2=6
    required_lessons = models.PositiveIntegerField(default=0)
    required_reviews = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.cefr_level} (#{self.order})"


class UserLessonProgress(models.Model):
    """Marks a lesson (Chapter) completed by a user — feeds the level engine."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_progress",
    )
    chapter = models.ForeignKey(
        "books.Chapter", on_delete=models.CASCADE, related_name="completions"
    )
    score = models.FloatField(null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "chapter")]

    def __str__(self):
        return f"{self.user} ✓ {self.chapter}"
