from django.conf import settings
from django.db import models


class HistoryLesson(models.Model):
    """A German-history lesson (Phase 18). Always-available (no Mon/Wed/Fri
    gating). Bilingual: the frontend shows English + German through A2 and
    German-only from B1. `quiz` holds the questions WITH answers; the serializer
    strips answers before sending, and the complete endpoint grades against it.
    """

    title = models.CharField(max_length=200)
    era = models.CharField(max_length=80, blank=True)  # grouping label
    order = models.PositiveIntegerField(default=0)
    body_en = models.TextField(blank=True)
    body_de = models.TextField()
    # [{"prompt": str, "options": [str, ...], "answer": str}]
    quiz = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class UserHistoryProgress(models.Model):
    """Marks a history lesson completed by a user (with the quiz score)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="history_progress",
    )
    lesson = models.ForeignKey(HistoryLesson, on_delete=models.CASCADE, related_name="completions")
    score = models.IntegerField(null=True, blank=True)  # % correct
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "lesson")]

    def __str__(self):
        return f"{self.user} ✓ {self.lesson}"
