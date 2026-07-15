from rest_framework import viewsets

from apps.accounts.levels import visible_levels_for

from .models import GrammarRule
from .serializers import GrammarRuleSerializer
from .unlocking import grammar_unlock_map


class GrammarRuleViewSet(viewsets.ModelViewSet):
    queryset = GrammarRule.objects.select_related("chapter").all()
    serializer_class = GrammarRuleSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # ≤-level rule (Spec v3): never expose grammar above the user's level.
        # Guests see the lowest level only.
        qs = qs.filter(chapter__cefr_level__in=visible_levels_for(self.request.user))
        chapter = self.request.query_params.get("chapter")
        category = self.request.query_params.get("category")
        if chapter:
            qs = qs.filter(chapter_id=chapter)
        if category:
            qs = qs.filter(category=category)
        # Ascending by book then Lektion number (overrides model's -created_at).
        return qs.order_by("chapter__book_id", "chapter__number", "id")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        user = self.request.user if self.request.user.is_authenticated else None
        ctx["grammar_unlock"] = grammar_unlock_map(user)
        return ctx
