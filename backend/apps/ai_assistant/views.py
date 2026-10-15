"""One-shot AI endpoints. Each validates its fields, calls a function in
`llm.py`, and returns {"content": "<text>"}.

Missing fields return 400; a missing Gemini key returns 503.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import IsPremium

from . import context, llm
from .serializers import AISettingsSerializer
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
    return _run(
        llm.chat,
        request.data["message"],
        request.data.get("history") or [],
        context.system_prompt(request.user),
    )


@api_view(["GET", "PUT"])
@permission_classes(_AI_PERMISSIONS)
def ai_settings(request):
    """GET: how the AI talks to me (defaults until saved). PUT: change it."""
    prefs = context.settings_for(request.user)
    if request.method == "PUT":
        serializer = AISettingsSerializer(prefs, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        prefs = serializer.instance
    data = AISettingsSerializer(prefs).data
    # What "By my level" means right now, so the page can say it.
    data["auto_language"] = context.reply_language(
        request.user, context.AISettings(reply_language="auto")
    )
    return Response(data)


@api_view(["GET"])
@permission_classes(_AI_PERMISSIONS)
def starters(request):
    """Chat starters from the learner's progress (no AI call)."""
    return Response(context.starters(request.user))
