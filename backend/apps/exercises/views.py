from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Exercise, ExerciseAttempt
from .serializers import ExerciseSerializer


def normalize(s: str) -> str:
    return (s or "").strip().lower()


def grade(exercise, user_answer):
    """Grade an attempt. Returns (is_correct, solution) where `solution` is a
    human/UI-friendly representation of the correct answer for the reveal."""
    t = exercise.exercise_type
    p = exercise.payload or {}

    if t == "multiple_choice":
        answer = p.get("answer", "")
        return normalize(str(user_answer)) == normalize(str(answer)), answer

    if t == "sentence_order":
        answer = p.get("answer", [])
        ua = user_answer if isinstance(user_answer, list) else []
        ok = [normalize(x) for x in ua] == [normalize(x) for x in answer]
        return ok, " ".join(answer)

    if t == "matching":
        # user_answer: {left: right} mapping; correct pairs in payload
        pairs = {normalize(a): normalize(b) for a, b in p.get("pairs", [])}
        ua = user_answer if isinstance(user_answer, dict) else {}
        ok = len(ua) == len(pairs) and all(
            pairs.get(normalize(k)) == normalize(v) for k, v in ua.items()
        )
        return ok, {a: b for a, b in p.get("pairs", [])}

    if t == "word_bank":
        answers = p.get("answers", [])
        ua = user_answer if isinstance(user_answer, list) else []
        ok = len(ua) == len(answers) and all(
            normalize(x) == normalize(y) for x, y in zip(ua, answers, strict=False)
        )
        return ok, answers

    # Simple text types.
    return normalize(str(user_answer)) == normalize(exercise.correct_answer), (
        exercise.correct_answer
    )


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.select_related("chapter").all()
    serializer_class = ExerciseSerializer

    def get_permissions(self):
        # Editing the shared exercise content requires an account; reading and
        # attempting (guests may practice) do not.
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        chapter = self.request.query_params.get("chapter")
        ex_type = self.request.query_params.get("type")
        if chapter:
            qs = qs.filter(chapter_id=chapter)
        if ex_type:
            qs = qs.filter(exercise_type=ex_type)
        return qs

    @action(detail=True, methods=["post"], url_path="attempt")
    def attempt(self, request, pk=None):
        exercise = self.get_object()
        user_answer = request.data.get("user_answer", "")
        is_correct, solution = grade(exercise, user_answer)

        ExerciseAttempt.objects.create(
            exercise=exercise,
            user=request.user if request.user.is_authenticated else None,
            user_answer=str(user_answer),
            is_correct=is_correct,
            ai_feedback="",
        )

        return Response(
            {
                "is_correct": is_correct,
                "correct_answer": solution,
                "explanation": exercise.explanation,
                "ai_feedback": "",
            }
        )
