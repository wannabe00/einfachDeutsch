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
