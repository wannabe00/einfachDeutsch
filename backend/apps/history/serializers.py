import re

from rest_framework import serializers

from .models import HistoryLesson

EXCERPT_LENGTH = 180


def _derive_excerpt(lesson: HistoryLesson) -> str:
    """First sentence-ish of the body, for lessons with no authored excerpt.

    Prefers English (the card is chrome, not the lesson) and strips markdown
    headings/emphasis so the teaser reads as prose.
    """
    body = (lesson.body_en or lesson.body_de or "").strip()
    if not body:
        return ""
    text = re.sub(r"[#*_>`]+", "", body)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= EXCERPT_LENGTH:
        return text
    clipped = text[:EXCERPT_LENGTH]
    # Cut on a word boundary rather than mid-word.
    return clipped[: clipped.rfind(" ")].rstrip(",;:") + "…"


class HistoryLessonListSerializer(serializers.ModelSerializer):
    """The article card: hero image + teaser (Phase 23.12)."""

    completed = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = HistoryLesson
        fields = [
            "id",
            "title",
            "era",
            "order",
            "completed",
            "cefr_level",
            "excerpt",
            "image_url",
        ]

    def get_completed(self, obj):
        return obj.id in self.context.get("completed_ids", set())

    def get_excerpt(self, obj) -> str:
        return obj.excerpt or _derive_excerpt(obj)


class HistoryLessonDetailSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField()

    class Meta:
        model = HistoryLesson
        fields = [
            "id",
            "title",
            "era",
            "body_en",
            "body_de",
            "quiz",
            "completed",
            "cefr_level",
            "image_url",
        ]

    def get_completed(self, obj):
        return obj.id in self.context.get("completed_ids", set())

    def get_quiz(self, obj):
        # Strip the answer key — the client only gets prompt + options.
        return [
            {"id": i, "prompt": q.get("prompt", ""), "options": q.get("options", [])}
            for i, q in enumerate(obj.quiz or [])
        ]
