from rest_framework import serializers

from .models import GrammarRule


class GrammarRuleSerializer(serializers.ModelSerializer):
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
        ]
