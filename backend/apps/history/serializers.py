import re

from rest_framework import serializers

from .models import CustomHistoryLesson, HistoryLesson
from .quiz import public_quiz

EXCERPT_LENGTH = 180


def _derive_excerpt(lesson: HistoryLesson) -> str:
    """First sentence-ish of the body, for lessons with no authored excerpt.

    Uses the German text (the lesson is read in German first) and strips
    markdown headings/emphasis so the teaser reads as prose.
    """
    body = (lesson.body_de or lesson.body_en or "").strip()
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
    """The article card: hero image + teaser."""

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
            "image_credit",
        ]

    def get_completed(self, obj):
        return obj.id in self.context.get("completed_ids", set())

    def get_quiz(self, obj):
        # Answers stripped, options shuffled (see history.quiz).
        return public_quiz(obj.quiz, str(obj.id))


class CustomLessonListSerializer(serializers.ModelSerializer):
    """An AI-written lesson as a card."""

    completed = serializers.SerializerMethodField()

    class Meta:
        model = CustomHistoryLesson
        fields = ["id", "title", "era", "excerpt", "image_url", "cefr_level", "completed"]

    def get_completed(self, obj) -> bool:
        return obj.score is not None


class CustomLessonDetailSerializer(serializers.ModelSerializer):
    """An AI-written lesson to read, in the same shape as a built-in one."""

    completed = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField()

    class Meta:
        model = CustomHistoryLesson
        fields = [
            "id",
            "topic",
            "title",
            "era",
            "body_en",
            "body_de",
            "quiz",
            "completed",
            "cefr_level",
            "image_url",
            "image_credit",
        ]

    def get_completed(self, obj) -> bool:
        return obj.score is not None

    def get_quiz(self, obj):
        return public_quiz(obj.quiz, f"custom-{obj.id}")
