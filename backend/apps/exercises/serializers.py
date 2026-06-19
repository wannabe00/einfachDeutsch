from rest_framework import serializers

from .models import Exercise, ExerciseAttempt


class ExerciseSerializer(serializers.ModelSerializer):
    """Default representation — solutions are intentionally omitted.

    `correct_answer` is never sent here, and answer fields are stripped from
    `payload`. The attempt endpoint reveals the solution and grades the answer.
    For interactive types, `payload` is shuffled/cleaned so the UI can render
    the exercise without seeing the solution.
    """

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
        p = dict(obj.payload or {})
        t = obj.exercise_type
        if t == "multiple_choice":
            # keep options, drop the answer
            return {"options": p.get("options", [])}
        if t == "matching":
            # send left + right separately (right shuffled) — no pairing given
            pairs = p.get("pairs", [])
            lefts = [pair[0] for pair in pairs]
            rights = [pair[1] for pair in pairs]
            return {"left": lefts, "right": sorted(rights)}
        if t == "sentence_order":
            return {"tokens": p.get("tokens", [])}
        if t == "word_bank":
            return {"text": p.get("text", ""), "bank": p.get("bank", [])}
        return {}


class ExerciseAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseAttempt
        fields = [
            "id",
            "exercise",
            "user_answer",
            "is_correct",
            "ai_feedback",
            "attempted_at",
        ]
