from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.levels import level_rank, visible_levels

from .models import ShowSuggestion
from .serializers import ShowSuggestionSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def suggestions(request):
    """Curated watch suggestions.

    Two independent gates: they **unlock** at `VIDEO_UNLOCK_MIN_LEVEL` (default
    B1, i.e. after finishing A2), and once unlocked they still obey the ≤-level
    rule (Spec v3) — you only see entries at or below your level.
    """
    min_level = settings.VIDEO_UNLOCK_MIN_LEVEL
    user_level = request.user.profile.cefr_level
    unlocked = level_rank(user_level) >= level_rank(min_level)

    data = {
        "unlocked": unlocked,
        "unlock_level": min_level,
        "current_level": user_level,
        "suggestions": [],
    }
    if unlocked:
        qs = ShowSuggestion.objects.filter(cefr_level__in=visible_levels(user_level))
        data["suggestions"] = ShowSuggestionSerializer(qs, many=True).data
    return Response(data)
