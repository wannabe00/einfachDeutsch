from datetime import timedelta

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    parser_classes,
    permission_classes,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .leveling import evaluate_level, grade_placement, public_questions
from .models import CEFR_LEVELS
from .scheduling import streak_status
from .serializers import UserDetailsSerializer

User = get_user_model()
VALID_LEVELS = {code for code, _ in CEFR_LEVELS}
USERNAME_COOLDOWN_DAYS = 30


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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def streak(request):
    """Streak, freeze tokens, and the Mon/Wed/Fri unlock schedule."""
    return Response(streak_status(request.user))


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update name/surname, birthday, phone, preferences, and (rate-limited)
    username. Level is intentionally NOT editable here."""
    user = request.user
    profile = user.profile
    data = request.data

    if "first_name" in data:
        user.first_name = str(data["first_name"]).strip()
    if "last_name" in data:
        user.last_name = str(data["last_name"]).strip()

    new_username = str(data.get("username", "")).strip()
    if new_username and new_username.lower() != user.username.lower():
        if len(new_username) < 3:
            return Response({"detail": "Username must be at least 3 characters."}, status=400)
        if User.objects.filter(username__iexact=new_username).exclude(pk=user.pk).exists():
            return Response({"detail": "That username is already taken."}, status=400)
        last = profile.username_changed_at
        if last and timezone.now() < last + timedelta(days=USERNAME_COOLDOWN_DAYS):
            nxt = (last + timedelta(days=USERNAME_COOLDOWN_DAYS)).date()
            return Response({"detail": f"You can change your username again on {nxt}."}, status=400)
        user.username = new_username
        profile.username_changed_at = timezone.now()

    if "birthday" in data:
        profile.birthday = data["birthday"] or None
    if "phone" in data:
        profile.phone = str(data.get("phone") or "").strip()
    if isinstance(data.get("preferences"), dict):
        prefs = profile.preferences or {}
        prefs.update(data["preferences"])
        profile.preferences = prefs

    user.save()
    profile.save()
    return Response(UserDetailsSerializer(user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_avatar(request):
    """Upload a profile picture to Cloudinary (server-side) and store the URL."""
    image = request.FILES.get("image")
    if image is None:
        return Response({"detail": "No image provided."}, status=400)
    if not settings.CLOUDINARY_CLOUD_NAME:
        return Response({"detail": "Image uploads aren't configured yet."}, status=503)
    try:
        import cloudinary.uploader

        result = cloudinary.uploader.upload(
            image,
            folder="einfachdeutsch/avatars",
            public_id=f"user_{request.user.id}",
            overwrite=True,
            transformation=[{"width": 256, "height": 256, "crop": "fill", "gravity": "face"}],
        )
        url = result.get("secure_url", "")
    except Exception:  # noqa: BLE001 — any upload/provider failure
        return Response({"detail": "Upload failed. Please try again."}, status=502)

    profile = request.user.profile
    profile.avatar_url = url
    profile.save(update_fields=["avatar_url"])
    return Response({"avatar_url": url})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_all(request):
    """Invalidate the user's auth token(s) — logs out everywhere."""
    Token.objects.filter(user=request.user).delete()
    return Response({"detail": "Logged out of all devices."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deactivate_account(request):
    """Soft-disable the account (reversible by an admin re-enabling it)."""
    user = request.user
    user.is_active = False
    user.save(update_fields=["is_active"])
    Token.objects.filter(user=user).delete()
    return Response({"detail": "Account deactivated."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """Permanently delete the account (optionally password-confirmed)."""
    password = request.data.get("password")
    if password is not None and not request.user.check_password(password):
        return Response({"detail": "Incorrect password."}, status=400)
    request.user.delete()
    return Response({"detail": "Account deleted."}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reset_progress(request):
    """Clear all of the user's learning progress (keeps the account)."""
    from apps.exercises.models import ExerciseAttempt
    from apps.history.models import UserHistoryProgress
    from apps.vocabulary.models import ReviewLog, WordProgress

    from .models import StreakRecord, UserLessonProgress

    user = request.user
    WordProgress.objects.filter(user=user).delete()
    ReviewLog.objects.filter(user=user).delete()
    ExerciseAttempt.objects.filter(user=user).delete()
    UserHistoryProgress.objects.filter(user=user).delete()
    UserLessonProgress.objects.filter(user=user).delete()
    StreakRecord.objects.filter(user=user).delete()
    return Response({"detail": "Progress reset."})


class GoogleLogin(SocialLoginView):
    """Exchange a Google OAuth `code` (sent by the SPA callback) for a DRF token.
    Creates the account on first sign-in (profile_complete stays False until
    onboarding)."""

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = f"{settings.FRONTEND_URL.rstrip('/')}/auth/callback/google"


class GitHubLogin(SocialLoginView):
    """Exchange a GitHub OAuth `code` for a DRF token (same flow as Google)."""

    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = f"{settings.FRONTEND_URL.rstrip('/')}/auth/callback/github"


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_onboarding(request):
    """First-run profile setup after a social sign-in: set username + password
    (so username/password login works) + name. Birthday/phone optional. The
    existing auth token stays valid after the password is set."""
    user = request.user
    profile = user.profile
    data = request.data

    username = str(data.get("username", "")).strip()
    password = data.get("password") or ""
    first_name = str(data.get("first_name", "")).strip()
    last_name = str(data.get("last_name", "")).strip()

    if len(username) < 3:
        return Response({"detail": "Username must be at least 3 characters."}, status=400)
    if User.objects.filter(username__iexact=username).exclude(pk=user.pk).exists():
        return Response({"detail": "That username is already taken."}, status=400)
    if len(password) < 8:
        return Response({"detail": "Password must be at least 8 characters."}, status=400)
    if not first_name or not last_name:
        return Response({"detail": "First and last name are required."}, status=400)

    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.set_password(password)
    user.save()

    profile.birthday = data.get("birthday") or None
    profile.phone = str(data.get("phone") or "").strip()
    profile.profile_complete = True
    if profile.username_changed_at is None:
        profile.username_changed_at = timezone.now()
    profile.save()

    return Response(UserDetailsSerializer(user).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_data(request):
    """Return the user's stored personal data as JSON (a simple data export)."""
    u = request.user
    p = u.profile
    return Response(
        {
            "email": u.email,
            "username": u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "birthday": p.birthday,
            "phone": p.phone,
            "cefr_level": p.cefr_level,
            "role": p.role,
            "joined": u.date_joined,
            "preferences": p.preferences,
        }
    )
