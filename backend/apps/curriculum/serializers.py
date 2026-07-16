from rest_framework import serializers

from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word

from . import grading
from .models import Lesson, LessonItem, Unit


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


class LessonItemSerializer(serializers.ModelSerializer):
    """One playable step. **Answers are stripped** — grading happens server-side
    and the solution is only revealed after an attempt."""

    content = serializers.SerializerMethodField()

    class Meta:
        model = LessonItem
        fields = ["id", "order", "kind", "content"]

    def get_content(self, item: LessonItem):
        if item.exercise_id and item.kind in {LessonItem.Kind.EXERCISE, LessonItem.Kind.DRILL}:
            # Shared with the level exam — one place strips answers.
            return grading.public_exercise(item.exercise)
        if item.word_id and item.kind == LessonItem.Kind.REVIEW:
            return {
                "word_id": item.word.id,
                "german": item.word.german,
                "english": item.word.english,
            }
        if item.grammar_rule_id and item.kind == LessonItem.Kind.GRAMMAR:
            rule = item.grammar_rule
            return {
                "grammar_id": rule.id,
                "title": rule.title,
                "category": rule.category,
                "content": rule.content,
                "example_sentences": rule.example_sentences,
            }
        return None


class LessonDetailSerializer(serializers.ModelSerializer):
    items = LessonItemSerializer(many=True, read_only=True)
    unit_id = serializers.IntegerField(source="unit.id", read_only=True)
    unit_title = serializers.CharField(source="unit.title", read_only=True)
    accent_color = serializers.CharField(source="unit.accent_color", read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id",
            "order",
            "title",
            "xp_reward",
            "unit_id",
            "unit_title",
            "accent_color",
            "items",
        ]
