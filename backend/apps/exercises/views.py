from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Exercise
from .serializers import ExerciseSerializer


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    """The shared exercises, read-only and without answers. Practising happens
    in the lesson player and in practice sets (curriculum.practice)."""

    queryset = Exercise.objects.select_related("chapter").all()
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        chapter = self.request.query_params.get("chapter")
        ex_type = self.request.query_params.get("type")
        if chapter:
            qs = qs.filter(chapter_id=chapter)
        if ex_type:
            qs = qs.filter(exercise_type=ex_type)
        return qs
