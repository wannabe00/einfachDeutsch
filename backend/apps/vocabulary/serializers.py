from rest_framework import serializers

from .models import Word, WordProgress


class WordProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordProgress
        fields = [
            "repetitions",
            "ease_factor",
            "interval",
            "next_review",
            "last_reviewed",
            "times_seen",
            "times_correct",
            "times_wrong",
            "lapses",
        ]


class WordSerializer(serializers.ModelSerializer):
    progress = WordProgressSerializer(read_only=True)

    class Meta:
        model = Word
        fields = [
            "id",
            "chapter",
            "english",
            "german",
            "notes",
            "created_at",
            "progress",
        ]
