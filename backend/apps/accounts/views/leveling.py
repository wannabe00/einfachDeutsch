"""Level + streak endpoints: set level, placement test, progression, streak."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..leveling import evaluate_level, local_level, public_test, score_objective
from ..models import CEFR_LEVELS
from ..scheduling import streak_status

VALID_LEVELS = {code for code, _ in CEFR_LEVELS}


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_level(request):
    """Set the user's CEFR level and mark onboarding complete."""
    level = str(request.data.get("cefr_level", "")).upper()
    if level not in VALID_LEVELS:
        return Response({"detail": "Invalid level."}, status=400)
    profile = request.user.profile
    profile.cefr_level = level
    profile.level_set = True
    profile.save(update_fields=["cefr_level", "level_set"])
    return Response({"cefr_level": level, "level_set": True})


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def placement_test(request):
    """GET: the test (grammar + reading + writing, shuffled, no answers).
    POST {answers:{id:choice}, writing:str}: score the MCQs locally, then ask
    Gemini for the final CEFR level — falling back to local scoring if the AI
    key/quota is unavailable."""
    if request.method == "GET":
        return Response(public_test())

    answers = request.data.get("answers")
    if not isinstance(answers, dict):
        return Response({"detail": "'answers' must be an object."}, status=400)
    writing = str(request.data.get("writing") or "")

    summary = score_objective(answers)
    result = {
        "suggested_level": local_level(summary),
        "source": "local",
        "rationale": "",
        "correct": summary["correct"],
        "total": summary["total"],
        "per_level": summary["per_level"],
    }

    try:
        from apps.ai_assistant.llm import AIConfigError, determine_level

        ai = determine_level(summary, writing)
        if ai.get("level") in VALID_LEVELS:
            result["suggested_level"] = ai["level"]
            result["source"] = "ai"
            result["rationale"] = ai.get("rationale", "")
    except AIConfigError:
        pass  # no key configured — keep the local result
    except Exception:  # noqa: BLE001 — any AI/parse failure falls back to local
        pass

    return Response(result)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def level_status(request):
    """Progression status: current level, requirements, and advance eligibility."""
    return Response(evaluate_level(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def streak(request):
    """Streak, freeze tokens, and the Mon/Wed/Fri unlock schedule."""
    return Response(streak_status(request.user))
