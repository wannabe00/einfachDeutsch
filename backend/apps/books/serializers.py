from rest_framework import serializers

from .models import Book, Chapter


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["id", "book", "number", "title", "description"]
        # book is set from the nested URL (/books/{id}/chapters/), not the body.
        read_only_fields = ["book"]


class BookSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "description", "created_at", "chapters"]
