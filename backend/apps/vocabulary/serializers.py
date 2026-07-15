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
    # The Word Bank groups by Level → part of speech (Phase 23.9). The level
    # comes from the word's chapter (a chapter is one Lektion).
    cefr_level = serializers.CharField(source="chapter.cefr_level", read_only=True)
    # True for words from a Lektion at the user's own level that they haven't
    # reached yet — shown blurred. The viewset supplies `locked_chapter_ids`.
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
        return obj.chapter_id in self.context.get("locked_chapter_ids", set())
