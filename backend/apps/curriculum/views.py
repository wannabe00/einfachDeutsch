from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word

from . import energy as energy_lib
from . import gating
from .models import LessonItem, PathLessonProgress, Unit
from .serializers import (
    PathUnitSerializer,
    UnitGrammarSerializer,
    UnitWordSerializer,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def path(request):
    """The user's learning path (Phase 23.4).

    Level-gated per Spec v3: only units **at or below** the user's level are
    returned — forward-level content is never exposed, not even locked. Within
    the user's own level the path is strictly linear; below it, everything is
    open as optional review.
    """
    user = request.user
    level = user.profile.cefr_level

    units = (
        Unit.objects.filter(cefr_level__in=gating.visible_levels(level))
        .order_by("cefr_level", "order")
        .prefetch_related("lessons")
    )

    states, next_lesson = gating.path_states(user, units)
    crowns = dict(PathLessonProgress.objects.filter(user=user).values_list("lesson_id", "crown"))

    # Attach the computed state/crown so the serializer can read them.
    for unit in units:
        for lesson in unit.lessons.all():
            lesson.state = states.get(lesson.id, "locked")
            lesson.crown = crowns.get(lesson.id, 0)

    premium = user.profile.has_premium
    return Response(
        {
            "level": level,
            "energy": {
                "current": energy_lib.current_energy(user),
                "max": energy_lib.ENERGY_MAX,
                "premium": premium,
                "seconds_until_next": energy_lib.seconds_until_next(user),
            },
            "next_up": (
                {
                    "lesson_id": next_lesson.id,
                    "lesson_title": next_lesson.title,
                    "unit_title": next_lesson.unit.title,
                }
                if next_lesson
                else None
            ),
            "units": PathUnitSerializer(units, many=True).data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unit_detail(request, unit_id: int):
    """One unit's page (Phase 23.4b): its lesson trail + review material.

    Review material comes from the unit's chapter — i.e. the whole Lektion's
    Wortschatz/grammar — so the panel is complete rather than only the handful
    of words its lessons happen to reference. Level-gated: a unit above the
    user's level is refused.
    """
    user = request.user
    unit = get_object_or_404(Unit.objects.prefetch_related("lessons"), pk=unit_id)

    if not gating.is_level_visible(user.profile.cefr_level, unit.cefr_level):
        raise PermissionDenied("This unit is above your level.")

    states, _ = gating.path_states(user, [unit])
    crowns = dict(PathLessonProgress.objects.filter(user=user).values_list("lesson_id", "crown"))
    for lesson in unit.lessons.all():
        lesson.state = states.get(lesson.id, "locked")
        lesson.crown = crowns.get(lesson.id, 0)

    # Prefer the unit's chapter (the whole Lektion's Wortschatz/grammar) so the
    # review panel is complete; fall back to whatever its lessons reference.
    if unit.chapter_id:
        words = Word.objects.filter(chapter_id=unit.chapter_id)
        rules = GrammarRule.objects.filter(chapter_id=unit.chapter_id)
    else:
        items = LessonItem.objects.filter(lesson__unit=unit)
        words = Word.objects.filter(
            id__in=items.exclude(word=None).values_list("word_id", flat=True)
        )
        rules = GrammarRule.objects.filter(
            id__in=items.exclude(grammar_rule=None).values_list("grammar_rule_id", flat=True)
        )

    data = PathUnitSerializer(unit).data
    data["words"] = UnitWordSerializer(words.order_by("id"), many=True).data
    data["grammar"] = UnitGrammarSerializer(rules.order_by("id"), many=True).data
    return Response(data)
