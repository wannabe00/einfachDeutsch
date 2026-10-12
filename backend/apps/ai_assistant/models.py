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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Most recently used first, matching the sidebar.
        ordering = ["-updated_at", "-id"]

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
