from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer, ChapterSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=["get", "post"])
    def chapters(self, request, pk=None):
        """List or create chapters for a single book.

        GET  /api/books/{id}/chapters/
        POST /api/books/{id}/chapters/
        """
        book = self.get_object()

        if request.method == "POST":
            serializer = ChapterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer = ChapterSerializer(book.chapters.all(), many=True)
        return Response(serializer.data)
