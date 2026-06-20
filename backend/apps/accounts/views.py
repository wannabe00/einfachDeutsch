from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .leveling import evaluate_level, grade_placement, public_questions
from .models import CEFR_LEVELS

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
    """GET: the question set (no answers). POST {answers:{id:choice}}: grade it."""
    if request.method == "GET":
        return Response({"questions": public_questions()})
    answers = request.data.get("answers")
    if not isinstance(answers, dict):
        return Response({"detail": "'answers' must be an object."}, status=400)
    return Response(grade_placement(answers))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def level_status(request):
    """Progression status: current level, requirements, and advance eligibility."""
    return Response(evaluate_level(request.user))
