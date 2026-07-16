from django.urls import path

from . import conversations, views

urlpatterns = [
    path("ai/suggest-words/", views.suggest_words, name="ai-suggest-words"),
    path("ai/explain-grammar/", views.explain_grammar, name="ai-explain-grammar"),
    path("ai/generate-exercises/", views.generate_exercises, name="ai-generate-exercises"),
    path("ai/check-answer/", views.check_answer, name="ai-check-answer"),
    # One-shot chat for the AI slide-over (nothing to resume).
    path("ai/chat/", views.chat, name="ai-chat"),
    # ChatGPT-style history for the AI Assistant page (Phase 23.13).
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
