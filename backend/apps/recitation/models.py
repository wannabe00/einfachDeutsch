from django.conf import settings
from django.db import models


class RecitationAttempt(models.Model):
    """A graded "retell it in your own words" attempt (Phase 16).

    The audio is NEVER stored — it's transcribed then discarded. We keep only
    the transcript + grading so the user has a history and we can enforce the
    per-user daily cap.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recitations",
    )
    source_text = models.TextField()
    transcript = models.TextField(blank=True)
    coverage_score = models.IntegerField(null=True, blank=True)  # 0–100
    feedback = models.JSONField(default=dict, blank=True)  # full structured result
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} recitation ({self.coverage_score}%) @ {self.created_at:%Y-%m-%d}"
