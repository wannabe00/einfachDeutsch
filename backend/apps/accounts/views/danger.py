"""Destructive account endpoints. Every one of them requires the account
password, so a stolen token alone can't wipe or delete an account."""

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..throttles import PasswordChangeThrottle


def _password_error(request):
    """Verify the password sent with a destructive request. Returns an error
    Response, or None when the action may proceed.

    Accounts that never finished onboarding have no password yet. They hold no
    data worth protecting, so they may proceed without one."""
    user = request.user
    if not user.has_usable_password():
        return None
    password = request.data.get("password") or ""
    if not password:
        return Response({"detail": "Your password is required for this action."}, status=400)
    if not user.check_password(password):
        return Response({"detail": "Incorrect password."}, status=400)
    return None


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_all(request):
    """Delete the user's auth tokens, logging them out on every device."""
    Token.objects.filter(user=request.user).delete()
    return Response({"detail": "Logged out of all devices."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([PasswordChangeThrottle])
def deactivate_account(request):
    """Soft-disable the account (reversible by an admin re-enabling it)."""
    error = _password_error(request)
    if error:
        return error
    user = request.user
    user.is_active = False
    user.save(update_fields=["is_active"])
    Token.objects.filter(user=user).delete()
    return Response({"detail": "Account deactivated."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([PasswordChangeThrottle])
def delete_account(request):
    """Permanently delete the account (password-confirmed)."""
    error = _password_error(request)
    if error:
        return error
    request.user.delete()
    return Response({"detail": "Account deleted."}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([PasswordChangeThrottle])
def reset_progress(request):
    """Clear all of the user's learning progress (keeps the account)."""
    from apps.curriculum.models import LessonDraft, LevelExamAttempt, PathLessonProgress
    from apps.exercises.models import ExerciseAttempt
    from apps.history.models import UserHistoryProgress
    from apps.vocabulary.models import ReviewLog, WordProgress

    from ..models import StreakRecord

    error = _password_error(request)
    if error:
        return error

    user = request.user
    WordProgress.objects.filter(user=user).delete()
    ReviewLog.objects.filter(user=user).delete()
    ExerciseAttempt.objects.filter(user=user).delete()
    UserHistoryProgress.objects.filter(user=user).delete()
    PathLessonProgress.objects.filter(user=user).delete()
    LessonDraft.objects.filter(user=user).delete()
    LevelExamAttempt.objects.filter(user=user).delete()
    StreakRecord.objects.filter(user=user).delete()
    return Response({"detail": "Progress reset."})
