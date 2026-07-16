"""Chat history (Phase 23.13).

ChatGPT-style per-user conversations so the AI Assistant can be resumed instead
of vanishing on refresh. Per-user data (never shared), and premium-gated like the
rest of AI — see accounts.permissions.IsPremium.

The one-shot `/ai/chat/` endpoint stays for the AI slide-over panel, which asks
throwaway questions and has nothing to resume.
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
        # Most recently used first — the sidebar order.
        ordering = ["-updated_at", "-id"]

    def __str__(self):
        return f"{self.user}: {self.title or 'Untitled'}"

    def apply_auto_title(self, first_message: str) -> None:
        """Title an untitled conversation from its first message (no AI call —
        it would cost a request per chat for a cosmetic string)."""
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
