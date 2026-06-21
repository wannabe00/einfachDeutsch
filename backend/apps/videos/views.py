from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ShowSuggestion
from .serializers import ShowSuggestionSerializer

CEFR_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]


def _order(level: str) -> int:
    return CEFR_ORDER.index(level) if level in CEFR_ORDER else 0


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def suggestions(request):
    """Curated watch suggestions, unlocked once the user reaches the configured
    level (default B1, i.e. after finishing A2). Shows entries at or below the
    user's level so they're level-appropriate."""
    min_level = settings.VIDEO_UNLOCK_MIN_LEVEL
    user_level = request.user.profile.cefr_level
    unlocked = _order(user_level) >= _order(min_level)

    data = {
        "unlocked": unlocked,
        "unlock_level": min_level,
        "current_level": user_level,
        "suggestions": [],
    }
    if unlocked:
        allowed = CEFR_ORDER[: _order(user_level) + 1]
        qs = ShowSuggestion.objects.filter(cefr_level__in=allowed)
        data["suggestions"] = ShowSuggestionSerializer(qs, many=True).data
    return Response(data)
