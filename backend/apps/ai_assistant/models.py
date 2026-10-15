"""Chat history.

Saved per-user conversations, so an AI Assistant chat survives a refresh and
can be resumed. Premium only, like the rest of AI (see
accounts.permissions.IsPremium).

The one-shot `/ai/chat/` endpoint is separate: it serves the slide-over panel,
which asks one-off questions and saves nothing.
"""

from django.conf import settings
from django.db import models

TITLE_MAX = 120


class Conversation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations"
    )
    # Auto-filled from the first user message; the user can rename it.
    title = models.CharField(max_length=TITLE_MAX, blank=True)
    pinned = models.BooleanField(default=False)
    # The learning tool the chat uses now (see context.MODES); set with each message.
    mode = models.CharField(max_length=12, default="chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Pinned first, then most recently used, matching the sidebar.
        ordering = ["-pinned", "-updated_at", "-id"]

    def __str__(self):
        return f"{self.user}: {self.title or 'Untitled'}"

    def apply_auto_title(self, first_message: str) -> None:
        """Title an untitled conversation from its first message. No AI call:
        that would cost a request per chat just for a label."""
        if self.title:
            return
        text = " ".join((first_message or "").split())
        if not text:
            return
        self.title = text if len(text) <= TITLE_MAX else text[: TITLE_MAX - 1].rstrip() + "…"


class Message(models.Model):
    class Role(models.TextChoices):
        USER = "user", "User"
        ASSISTANT = "assistant", "Assistant"

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=10, choices=Role.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return f"[{self.role}] {self.content[:60]}"


class AISettings(models.Model):
    """How the AI talks to one learner (premium). Sent with every chat as part
    of the system prompt; see context.system_prompt."""

    class ReplyLanguage(models.TextChoices):
        AUTO = "auto", "By my level"
        ENGLISH = "en", "English"
        MIXED = "mixed", "Mixed"
        GERMAN = "de", "German"

    class Tone(models.TextChoices):
        FRIENDLY = "friendly", "Friendly tutor"
        STRICT = "strict", "Strict teacher"

    class Corrections(models.TextChoices):
        MAJOR = "major", "Only big mistakes"
        ALL = "all", "Every mistake"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_settings"
    )
    reply_language = models.CharField(
        max_length=5, choices=ReplyLanguage.choices, default=ReplyLanguage.AUTO
    )
    tone = models.CharField(max_length=10, choices=Tone.choices, default=Tone.FRIENDLY)
    corrections = models.CharField(
        max_length=5, choices=Corrections.choices, default=Corrections.MAJOR
    )
    interests = models.CharField(max_length=200, blank=True)
    about = models.CharField(max_length=500, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.reply_language}, {self.tone}"
