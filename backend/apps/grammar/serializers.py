from rest_framework import serializers

from .models import GrammarRule


class GrammarRuleSerializer(serializers.ModelSerializer):
    # Grammar is grouped Level → topic (Phase 23.10). The level comes from the
    # rule's chapter (a chapter is one Lektion).
    cefr_level = serializers.CharField(source="chapter.cefr_level", read_only=True)
    # Locked until the lesson that teaches it is completed. The viewset supplies
    # `grammar_unlock` (see grammar.unlocking); rules no lesson teaches are open.
    locked = serializers.SerializerMethodField()
    unlock_lesson = serializers.SerializerMethodField()

    class Meta:
        model = GrammarRule
        fields = [
            "id",
            "chapter",
            "title",
            "category",
            "content",
            "example_sentences",
            "created_at",
            "cefr_level",
            "locked",
            "unlock_lesson",
        ]

    def _entry(self, obj):
        return self.context.get("grammar_unlock", {}).get(obj.id)

    def get_locked(self, obj) -> bool:
        entry = self._entry(obj)
        return bool(entry and entry["locked"])

    def get_unlock_lesson(self, obj):
        """Which lesson unlocks this topic — powers the "next topic" indicator.
        Null once unlocked, or for topics no lesson teaches."""
        entry = self._entry(obj)
        if not entry or not entry["locked"]:
            return None
        return entry["lesson"]
