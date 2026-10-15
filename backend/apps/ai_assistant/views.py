"""One-shot AI endpoints. Each validates its fields, calls a function in
`llm.py`, and returns {"content": "<text>"}.

Missing fields return 400; a missing Gemini key returns 503.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import IsPremium

from . import llm
from .throttles import AIBurstThrottle, AIDailyThrottle

# AI spends the owner's Gemini quota and is what premium pays for, so every
# endpoint is premium-only and rate-limited. Exercise grading itself is local,
# which is why free users still get graded.
_AI_PERMISSIONS = [IsAuthenticated, IsPremium]
_AI_THROTTLES = [AIBurstThrottle, AIDailyThrottle]


def _missing_fields_response(data, *fields):
    """A 400 naming any blank required fields, or None if all are present."""
    missing = [f for f in fields if not str(data.get(f, "")).strip()]
    if not missing:
        return None
    return Response(
        {"detail": f"Missing fields: {', '.join(missing)}"},
        status=status.HTTP_400_BAD_REQUEST,
    )


def _run(fn, *args):
    try:
        return Response({"content": fn(*args)})
    except llm.AIConfigError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["POST"])
@permission_classes(_AI_PERMISSIONS)
@throttle_classes(_AI_THROTTLES)
def chat(request):
    error = _missing_fields_response(request.data, "message")
    if error:
        return error
    return _run(llm.chat, request.data["message"], request.data.get("history") or [])
