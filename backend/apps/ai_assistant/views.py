"""AI endpoints. Each view validates required fields, calls an llm.py
function, and returns {"content": "<text>"}. Missing fields -> 400.
If the API key is absent -> 503 with a clear message.
"""

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import IsPremium

from . import llm
from .throttles import AIBurstThrottle, AIDailyThrottle

# AI is premium-only (Spec v3) — it spends the owner's Gemini quota and is the
# paid tier's promise — and rate-limited per user. Applied to every endpoint
# below via these decorator stacks. Exercise grading stays deterministic/local,
# so free users are still graded.
_AI_PERMISSIONS = [IsAuthenticated, IsPremium]
_AI_THROTTLES = [AIBurstThrottle, AIDailyThrottle]


def _missing(data, *fields):
    return [f for f in fields if not str(data.get(f, "")).strip()]


def _run(fn, *args):
    try:
        return Response({"content": fn(*args)})
    except llm.AIConfigError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["POST"])
@permission_classes(_AI_PERMISSIONS)
@throttle_classes(_AI_THROTTLES)
def suggest_words(request):
    missing = _missing(request.data, "chapter_title")
    if missing:
        return Response(
            {"detail": f"Missing fields: {', '.join(missing)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    count = int(request.data.get("count") or 10)
    return _run(
        llm.suggest_words,
        request.data["chapter_title"],
        request.data.get("description", ""),
        count,
    )


@api_view(["POST"])
@permission_classes(_AI_PERMISSIONS)
@throttle_classes(_AI_THROTTLES)
def explain_grammar(request):
    missing = _missing(request.data, "topic")
    if missing:
        return Response(
            {"detail": f"Missing fields: {', '.join(missing)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return _run(llm.explain_grammar, request.data["topic"])


@api_view(["POST"])
@permission_classes(_AI_PERMISSIONS)
@throttle_classes(_AI_THROTTLES)
def generate_exercises(request):
    missing = _missing(request.data, "chapter_title")
    if missing:
        return Response(
            {"detail": f"Missing fields: {', '.join(missing)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return _run(
        llm.generate_exercises,
        request.data["chapter_title"],
        request.data.get("word_list", ""),
    )


@api_view(["POST"])
@permission_classes(_AI_PERMISSIONS)
@throttle_classes(_AI_THROTTLES)
def check_answer(request):
    missing = _missing(request.data, "prompt", "correct_answer", "user_answer")
    if missing:
        return Response(
            {"detail": f"Missing fields: {', '.join(missing)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return _run(
        llm.check_exercise_answer,
        request.data["prompt"],
        request.data["correct_answer"],
        request.data["user_answer"],
    )


@api_view(["POST"])
@permission_classes(_AI_PERMISSIONS)
@throttle_classes(_AI_THROTTLES)
def chat(request):
    missing = _missing(request.data, "message")
    if missing:
        return Response(
            {"detail": f"Missing fields: {', '.join(missing)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    history = request.data.get("history") or []
    return _run(llm.chat, request.data["message"], history)
