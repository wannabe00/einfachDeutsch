from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.levels import level_rank, visible_levels_for

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
        if self.request.user.is_authenticated:
            # Signed-in users only ever see topics they've learned. Imported
            # here so the grammar app doesn't hard-depend on curriculum.
            from apps.curriculum.learned import learned_rule_ids

            qs = qs.filter(id__in=learned_rule_ids(self.request.user))
        chapter = self.request.query_params.get("chapter")
        category = self.request.query_params.get("category")
        if chapter:
            qs = qs.filter(chapter_id=chapter)
        if category:
            qs = qs.filter(category=category)
        # Ascending by book then Lektion number (overrides model's -created_at).
        return qs.order_by("chapter__book_id", "chapter__number", "id")

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def next(self, request):
        """The next topic on the user's path and the lesson that teaches it,
        for the Grammar page's one "coming up" line: `{"next": ...}`, null when
        there's none."""
        from apps.curriculum.learned import learned_rule_ids, teaching_lessons

        user = request.user
        rules = GrammarRule.objects.filter(
            chapter__cefr_level__in=visible_levels_for(user)
        ).exclude(id__in=learned_rule_ids(user))
        lessons = teaching_lessons(rules.values_list("id", flat=True))
        if not lessons:
            return Response({"next": None})

        def path_position(item):
            unit = item[1].unit
            return (level_rank(unit.cefr_level), unit.order, item[1].order)

        rule_id, lesson = min(lessons.items(), key=path_position)
        return Response(
            {
                "next": {
                    "title": GrammarRule.objects.get(pk=rule_id).title,
                    "lesson": {
                        "title": lesson.title,
                        "unit_id": lesson.unit.id,
                        "unit_order": lesson.unit.order,
                        "unit_title": lesson.unit.title,
                    },
                }
            }
        )
