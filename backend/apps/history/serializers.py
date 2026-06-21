from rest_framework import serializers

from .models import HistoryLesson


class HistoryLessonListSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    class Meta:
        model = HistoryLesson
        fields = ["id", "title", "era", "order", "completed"]

    def get_completed(self, obj):
        return obj.id in self.context.get("completed_ids", set())


class HistoryLessonDetailSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField()

    class Meta:
        model = HistoryLesson
        fields = ["id", "title", "era", "body_en", "body_de", "quiz", "completed"]

    def get_completed(self, obj):
        return obj.id in self.context.get("completed_ids", set())

    def get_quiz(self, obj):
        # Strip the answer key — the client only gets prompt + options.
        return [
            {"id": i, "prompt": q.get("prompt", ""), "options": q.get("options", [])}
            for i, q in enumerate(obj.quiz or [])
        ]
