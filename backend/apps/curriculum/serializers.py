from rest_framework import serializers

from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word

from .models import Lesson, Unit


class PathLessonSerializer(serializers.ModelSerializer):
    """A lesson node on the path. `state` and `crown` are attached by the view
    (see gating.path_states) rather than stored on the model."""

    state = serializers.CharField(read_only=True)
    crown = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "order", "title", "xp_reward", "state", "crown"]


class PathUnitSerializer(serializers.ModelSerializer):
    lessons = PathLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ["id", "cefr_level", "order", "title", "theme", "accent_color", "lessons"]


class UnitWordSerializer(serializers.ModelSerializer):
    """Light vocab shape for the unit page's review panel (no SRS state)."""

    class Meta:
        model = Word
        fields = ["id", "german", "english"]


class UnitGrammarSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarRule
        fields = ["id", "title", "category", "content", "example_sentences"]
