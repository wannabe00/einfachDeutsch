from django.conf import settings
from django.db import models
from django.utils import timezone

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
    # False right after a Google/GitHub signup; set True once the user has
    # picked a username + password + name in onboarding. Gates the welcome flow.
    profile_complete = models.BooleanField(default=False)
    # Set once the user has chosen/confirmed their level (onboarding). Until
    # then the frontend shows the level picker / placement test.
    level_set = models.BooleanField(default=False)
    # Profile fields (name/surname live on the auth User as first_name/last_name).
    birthday = models.DateField(null=True, blank=True)
    avatar_url = models.URLField(blank=True)
    # Throttles username changes (allowed once every 30 days).
    username_changed_at = models.DateTimeField(null=True, blank=True)
    # Prefs as JSON (only daily_goal is used now; older keys may linger), so new
    # settings don't need migrations.
    preferences = models.JSONField(default=dict, blank=True)
    # Premium. Until payments exist, `is_premium` is set by hand in the admin.
    # `premium_until` covers the 7-day trial and, later, the end of a paid
    # subscription. `trial_started_at` records that the trial was used.
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(null=True, blank=True)
    trial_started_at = models.DateTimeField(null=True, blank=True)
    # Two-factor login with an authenticator app (accounts/totp.py). The secret
    # is set during setup and only counts once `totp_enabled`; backup codes are
    # stored hashed; `totp_last_step` stops a code being used twice.
    totp_secret = models.CharField(max_length=64, blank=True)
    totp_enabled = models.BooleanField(default=False)
    totp_backup_codes = models.JSONField(default=list, blank=True)
    totp_last_step = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def has_premium(self) -> bool:
        """True if the user currently has premium access (timed subscription/
        trial still active, or a manual no-expiry admin flag)."""
        if self.premium_until and self.premium_until > timezone.now():
            return True
        return self.is_premium and self.premium_until is None

    def __str__(self):
        return f"{self.user} ({self.cefr_level})"


class StreakRecord(models.Model):
    """Daily-practice streak + freeze tokens. One row per user.

    A streak only breaks on a missed scheduled day (Mon/Wed/Fri) when no freeze
    token is left; otherwise a freeze is used up automatically. Defaults live
    in settings (STREAK_*).
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="streak"
    )
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    freeze_tokens_available = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}: {self.current_streak} days ({self.freeze_tokens_available} freezes)"
