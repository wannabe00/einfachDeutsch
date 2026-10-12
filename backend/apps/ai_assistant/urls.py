from django.urls import path

from . import conversations, views

urlpatterns = [
    path("ai/check-answer/", views.check_answer, name="ai-check-answer"),
    # One-shot chat for the slide-over panel; nothing is saved.
    path("ai/chat/", views.chat, name="ai-chat"),
    # Saved conversations for the AI Assistant page.
    path("ai/conversations/", conversations.conversations, name="ai-conversations"),
    path(
        "ai/conversations/<int:pk>/",
        conversations.conversation_detail,
        name="ai-conversation-detail",
    ),
    path(
        "ai/conversations/<int:pk>/messages/",
        conversations.conversation_messages,
        name="ai-conversation-messages",
    ),
]
