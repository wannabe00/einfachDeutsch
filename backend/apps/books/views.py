from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer, ChapterSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """Books and their chapters, read-only. The owner adds books through the
    seed commands and the Django admin, never through the app."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=["get"])
    def chapters(self, request, pk=None):
        """GET /api/books/{id}/chapters/"""
        serializer = ChapterSerializer(self.get_object().chapters.all(), many=True)
        return Response(serializer.data)
