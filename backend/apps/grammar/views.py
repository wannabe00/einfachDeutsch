from rest_framework import viewsets

from .models import GrammarRule
from .serializers import GrammarRuleSerializer


class GrammarRuleViewSet(viewsets.ModelViewSet):
    queryset = GrammarRule.objects.select_related("chapter").all()
    serializer_class = GrammarRuleSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        chapter = self.request.query_params.get("chapter")
        category = self.request.query_params.get("category")
        if chapter:
            qs = qs.filter(chapter_id=chapter)
        if category:
            qs = qs.filter(category=category)
        # Ascending by book then Lektion number (overrides model's -created_at).
        return qs.order_by("chapter__book_id", "chapter__number", "id")
