from rest_framework import viewsets

from apps.accounts.levels import visible_levels_for

from .models import GrammarRule
from .serializers import GrammarRuleSerializer


class GrammarRuleViewSet(viewsets.ModelViewSet):
    queryset = GrammarRule.objects.select_related("chapter").all()
    serializer_class = GrammarRuleSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # ≤-level rule: never expose grammar above the user's level.
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
        if self.request.user.is_authenticated:
            # Imported here so the grammar app doesn't hard-depend on curriculum.
            from apps.curriculum.learned import learned_rule_ids, teaching_lessons

            learned = learned_rule_ids(self.request.user)
            ctx["learned_rule_ids"] = learned
            ctx["teaching_lessons"] = teaching_lessons(
                self.get_queryset().exclude(id__in=learned).values_list("id", flat=True)
            )
        return ctx
