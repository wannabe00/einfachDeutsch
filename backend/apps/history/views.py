from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.levels import visible_levels_for
from apps.accounts.permissions import IsPremium
from apps.ai_assistant.llm import AIConfigError
from apps.ai_assistant.throttles import AIBurstThrottle, AIDailyThrottle

from . import custom
from .models import CustomHistoryLesson, HistoryLesson, UserHistoryProgress
from .quiz import grade_quiz
from .serializers import (
    CustomLessonDetailSerializer,
    CustomLessonListSerializer,
    HistoryLessonDetailSerializer,
    HistoryLessonListSerializer,
)


class HistoryLessonViewSet(viewsets.ReadOnlyModelViewSet):
    """Always-available German-history lessons. Account-only (the EN/DE language
    switch depends on the user's CEFR level)."""

    queryset = HistoryLesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ≤-level rule: a B1 user never sees C1 history.
        return super().get_queryset().filter(cefr_level__in=visible_levels_for(self.request.user))

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

        result = grade_quiz(lesson.quiz, answers)
        UserHistoryProgress.objects.update_or_create(
            user=request.user, lesson=lesson, defaults={"score": result["score"]}
        )
        return Response(result)


class CustomLessonViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """History lessons the AI writes on request (premium). See history.custom.

    GET    /api/history/custom/            your lessons
    POST   /api/history/custom/chat/       one turn of the topic conversation
    POST   /api/history/custom/            write a lesson on the agreed topic
    GET    /api/history/custom/{id}/       read one
    POST   /api/history/custom/{id}/complete/   grade its quiz
    DELETE /api/history/custom/{id}/
    """

    permission_classes = [IsAuthenticated, IsPremium]

    def get_queryset(self):
        return CustomHistoryLesson.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return CustomLessonListSerializer if self.action == "list" else CustomLessonDetailSerializer

    def get_throttles(self):
        if self.action in ("chat", "create"):
            return [AIBurstThrottle(), AIDailyThrottle()]
        return super().get_throttles()

    def _ai(self, fn, *args):
        try:
            return fn(*args)
        except AIConfigError as err:
            raise custom.CustomLessonError(str(err), status.HTTP_503_SERVICE_UNAVAILABLE) from err

    def handle_exception(self, exc):
        if isinstance(exc, custom.CustomLessonError):
            return Response({"detail": str(exc)}, status=exc.status)
        return super().handle_exception(exc)

    @action(detail=False, methods=["post"])
    def chat(self, request):
        return Response(self._ai(custom.guide, request.data.get("messages")))

    def create(self, request):
        lesson = self._ai(custom.create_lesson, request.user, request.data.get("topic"))
        return Response(CustomLessonDetailSerializer(lesson).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        lesson = self.get_object()
        answers = request.data.get("answers") or {}
        if not isinstance(answers, dict):
            return Response({"detail": "'answers' must be an object."}, status=400)
        result = grade_quiz(lesson.quiz, answers)
        lesson.score = result["score"]
        lesson.save(update_fields=["score"])
        return Response(result)
