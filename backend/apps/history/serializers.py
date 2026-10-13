import random
import re

from rest_framework import serializers

from .models import HistoryLesson

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
        # Strip the answers; the client only gets each prompt and its options.
        # The content lists the right answer first, so the options are
        # shuffled, the same way every time for a given question.
        quiz = []
        for i, q in enumerate(obj.quiz or []):
            options = list(q.get("options", []))
            random.Random(f"{obj.id}-{i}").shuffle(options)
            quiz.append({"id": i, "prompt": q.get("prompt", ""), "options": options})
        return quiz
