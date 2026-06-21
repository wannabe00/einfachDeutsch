from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import HistoryLesson, UserHistoryProgress
from .serializers import HistoryLessonDetailSerializer, HistoryLessonListSerializer


class HistoryLessonViewSet(viewsets.ReadOnlyModelViewSet):
    """Always-available German-history lessons. Account-only (the EN/DE language
    switch depends on the user's CEFR level)."""

    queryset = HistoryLesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return HistoryLessonListSerializer
        return HistoryLessonDetailSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["completed_ids"] = set(
            UserHistoryProgress.objects.filter(user=self.request.user).values_list(
                "lesson_id", flat=True
            )
        )
        return ctx

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        lesson = self.get_object()
        answers = request.data.get("answers") or {}
        if not isinstance(answers, dict):
            return Response({"detail": "'answers' must be an object."}, status=400)

        quiz = lesson.quiz or []
        results = []
        correct = 0
        for i, q in enumerate(quiz):
            chosen = str(answers.get(str(i), answers.get(i, ""))).strip()
            ok = chosen == str(q.get("answer", "")).strip()
            correct += 1 if ok else 0
            results.append({"id": i, "correct": ok, "answer": q.get("answer", "")})

        total = len(quiz)
        score = round(correct / total * 100) if total else 100

        UserHistoryProgress.objects.update_or_create(
            user=request.user, lesson=lesson, defaults={"score": score}
        )
        return Response({"score": score, "correct": correct, "total": total, "results": results})
