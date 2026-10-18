from django.conf import settings
from django.db import models

from apps.accounts.models import CEFR_LEVELS


class Talk(models.Model):
    """One spoken conversation with the AI, like the Goethe speaking exam (see
    apps.talk.views), and its report, kept so the learner can read it again."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="talks"
    )
    level = models.CharField(max_length=2, choices=CEFR_LEVELS)
    # [{"role": "user" | "ai", "text": str}], sent by the browser at the end.
    transcript = models.JSONField(default=list, blank=True)
    # summary, corrections, phrases, new_words, practise (see llm.talk_report).
    report = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    # Set when the learner removes the talk: its transcript and report are wiped,
    # but the row stays so the daily cap still counts it.
    removed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at", "-id"]

    def __str__(self):
        return f"{self.user} · talk {self.started_at:%Y-%m-%d %H:%M}"
