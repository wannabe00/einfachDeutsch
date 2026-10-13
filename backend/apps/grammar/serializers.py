from rest_framework import serializers

from .models import GrammarRule


class GrammarRuleSerializer(serializers.ModelSerializer):
    # Grammar is grouped Level → topic. The level comes from the
    # rule's chapter (a chapter is one Lektion).
    cefr_level = serializers.CharField(source="chapter.cefr_level", read_only=True)
    # Locked until the user has learned it (see curriculum.learned). The viewset
    # supplies `learned_rule_ids` for signed-in users; guests see nothing locked.
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

    def get_locked(self, obj) -> bool:
        learned = self.context.get("learned_rule_ids")
        return learned is not None and obj.id not in learned

    def get_unlock_lesson(self, obj):
        """The lesson that teaches this topic, used for the "next topic" hint.
        Null once learned, or for topics no lesson teaches."""
        if not self.get_locked(obj):
            return None
        lesson = self.context.get("teaching_lessons", {}).get(obj.id)
        if lesson is None:
            return None
        unit = lesson.unit
        return {
            "id": lesson.id,
            "title": lesson.title,
            "unit_id": unit.id,
            "unit_title": unit.title,
            "unit_order": unit.order,
            "lesson_order": lesson.order,
        }
