from rest_framework import serializers

from .models import GrammarRule


class GrammarRuleSerializer(serializers.ModelSerializer):
    # Grammar is grouped Level → topic. The level comes from the
    # rule's chapter (a chapter is one Lektion).
    cefr_level = serializers.CharField(source="chapter.cefr_level", read_only=True)

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
        ]
