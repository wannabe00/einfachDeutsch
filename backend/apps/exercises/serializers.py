from rest_framework import serializers

from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    """An exercise without its answers: `correct_answer` is never sent and the
    payload is stripped the same way the lesson player strips it."""

    payload = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = [
            "id",
            "chapter",
            "exercise_type",
            "prompt",
            "payload",
            "hint",
            "explanation",
            "source",
            "created_at",
        ]

    def get_payload(self, obj):
        # Imported here so the exercises app doesn't hard-depend on curriculum.
        from apps.curriculum.grading import public_exercise

        return public_exercise(obj)["payload"]
