from django.urls import path

from . import views

urlpatterns = [
    path("ai/suggest-words/", views.suggest_words, name="ai-suggest-words"),
    path("ai/explain-grammar/", views.explain_grammar, name="ai-explain-grammar"),
    path("ai/generate-exercises/", views.generate_exercises, name="ai-generate-exercises"),
    path("ai/check-answer/", views.check_answer, name="ai-check-answer"),
    path("ai/chat/", views.chat, name="ai-chat"),
]
