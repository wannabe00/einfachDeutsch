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
    # Per-user SM-2 state for the requesting user, or null for guests / words the
    # user has never reviewed. The viewset prefetches it into `user_progress`
    # (a list with 0 or 1 item) to avoid an N+1 query.
    progress = serializers.SerializerMethodField()
    # The Word Bank groups by Level → part of speech. The level
    # comes from the word's chapter (a chapter is one Lektion).
    cefr_level = serializers.CharField(source="chapter.cefr_level", read_only=True)
    # True for words the user hasn't learned yet (see curriculum.learned); the
    # UI shows them blurred. The viewset supplies `learned_word_ids` for
    # signed-in users; guests see nothing locked.
    locked = serializers.SerializerMethodField()

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
            "cefr_level",
            "part_of_speech",
            "locked",
        ]

    def get_progress(self, obj):
        records = getattr(obj, "user_progress", None)
        if records:
            return WordProgressSerializer(records[0]).data
        return None

    def get_locked(self, obj) -> bool:
        learned = self.context.get("learned_word_ids")
        return learned is not None and obj.id not in learned
