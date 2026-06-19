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


class UserProfile(models.Model):
    """Per-user account state. One row per auth User."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    cefr_level = models.CharField(max_length=2, choices=CEFR_LEVELS, default="A1")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} ({self.cefr_level})"
