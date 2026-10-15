from django.urls import path

from . import conversations, views

urlpatterns = [
    # One-shot chat for the slide-over panel; nothing is saved.
    path("ai/chat/", views.chat, name="ai-chat"),
    # How the AI talks to the learner, and chat starters from their progress.
    path("ai/settings/", views.ai_settings, name="ai-settings"),
    path("ai/starters/", views.starters, name="ai-starters"),
    # Saved conversations for the AI Assistant page.
    path("ai/conversations/", conversations.conversations, name="ai-conversations"),
    path(
        "ai/conversations/<int:pk>/",
        conversations.conversation_detail,
        name="ai-conversation-detail",
    ),
    path(
        "ai/conversations/<int:pk>/retry/",
        conversations.conversation_retry,
        name="ai-conversation-retry",
    ),
    path(
        "ai/conversations/<int:pk>/messages/",
        conversations.conversation_messages,
        name="ai-conversation-messages",
    ),
]
