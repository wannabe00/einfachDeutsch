from rest_framework import serializers

from .models import SavedWord, Word, WordProgress


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
    # The Word Bank groups words by topic: the unit (Lektion) that teaches them,
    # or the chapter a user added them to.
    topic = serializers.SerializerMethodField()
    # Nouns note their plural as "Pl. die Tische"; split out for display.
    plural = serializers.SerializerMethodField()

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
            "topic",
            "plural",
        ]

    def get_progress(self, obj):
        records = getattr(obj, "user_progress", None)
        if records:
            return WordProgressSerializer(records[0]).data
        return None

    def get_topic(self, obj):
        # `chapter__units` is prefetched by the viewset.
        unit = next(iter(obj.chapter.units.all()), None)
        if unit is None:
            return {"key": f"c{obj.chapter_id}", "title": obj.chapter.title, "order": None}
        return {"key": f"u{unit.id}", "title": unit.title, "order": unit.order}

    def get_plural(self, obj) -> str:
        notes = obj.notes or ""
        return notes.removeprefix("Pl.").strip() if notes.startswith("Pl.") else ""


ARTICLES = ("der", "die", "das")


def capitalize_noun(german: str) -> str:
    """'der hund' -> 'der Hund': German nouns always show capitalised."""
    head, _, rest = " ".join(german.split()).partition(" ")
    if head.lower() in ARTICLES and rest:
        return f"{head.lower()} {rest[:1].upper()}{rest[1:]}"
    return f"{head} {rest}".strip()


class SavedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedWord
        fields = ["id", "german", "english", "notes", "created_at"]

    def validate_german(self, value):
        value = capitalize_noun(value)
        if not value:
            raise serializers.ValidationError("Write the German word.")
        return value
