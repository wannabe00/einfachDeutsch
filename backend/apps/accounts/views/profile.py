"""Profile endpoints: update profile, avatar upload, onboarding, data export."""

import re
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.decorators import (
    api_view,
    parser_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers import UserDetailsSerializer
from ..throttles import OnboardingThrottle

User = get_user_model()
USERNAME_COOLDOWN_DAYS = 30

# Only these keys may live in UserProfile.preferences (S7 — no arbitrary JSON).
ALLOWED_PREFERENCE_KEYS = {
    "daily_goal",
    "reminder_time",
    "weekdays",
    "notify_streak",
    "notify_unlock",
    "language",
    "timezone",
}
MAX_PREFERENCES_CHARS = 2000

# Loose international format: optional +, then digits/spaces/()- (S9).
PHONE_RE = re.compile(r"^\+?[0-9 ()\-]{5,20}$")

MAX_AVATAR_MB = 5


def _validate_username_change(user, profile, new_username):
    """Shared username rules (length, uniqueness, 30-day cooldown).
    Returns an error Response or None."""
    if len(new_username) < 3:
        return Response({"detail": "Username must be at least 3 characters."}, status=400)
    if User.objects.filter(username__iexact=new_username).exclude(pk=user.pk).exists():
        return Response({"detail": "That username is already taken."}, status=400)
    last = profile.username_changed_at
    if last and timezone.now() < last + timedelta(days=USERNAME_COOLDOWN_DAYS):
        nxt = (last + timedelta(days=USERNAME_COOLDOWN_DAYS)).date()
        return Response({"detail": f"You can change your username again on {nxt}."}, status=400)
    return None


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
        error = _validate_username_change(user, profile, new_username)
        if error:
            return error
        user.username = new_username
        profile.username_changed_at = timezone.now()

    if "birthday" in data:
        profile.birthday = data["birthday"] or None
    if "phone" in data:
        phone = str(data.get("phone") or "").strip()
        if phone and not PHONE_RE.match(phone):
            return Response({"detail": "Enter a valid phone number."}, status=400)
        profile.phone = phone
    if isinstance(data.get("preferences"), dict):
        incoming = data["preferences"]
        unknown = set(incoming) - ALLOWED_PREFERENCE_KEYS
        if unknown:
            return Response(
                {"detail": f"Unknown preference keys: {', '.join(sorted(unknown))}."},
                status=400,
            )
        merged = {**(profile.preferences or {}), **incoming}
        if len(str(merged)) > MAX_PREFERENCES_CHARS:
            return Response({"detail": "Preferences payload too large."}, status=400)
        profile.preferences = merged

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
    # S4: don't stream arbitrary files to Cloudinary.
    if image.size > MAX_AVATAR_MB * 1024 * 1024:
        return Response({"detail": f"Image too large (max {MAX_AVATAR_MB} MB)."}, status=400)
    if not (image.content_type or "").startswith("image/"):
        return Response({"detail": "File must be an image."}, status=400)
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
@throttle_classes([OnboardingThrottle])
def complete_onboarding(request):
    """First-run profile setup after a social sign-in: set username + password
    (so username/password login works) + name. Birthday/phone optional. The
    existing auth token stays valid after the password is set."""
    user = request.user
    profile = user.profile

    # S1: one-shot only. Re-running would let a stolen token change the
    # username + password without knowing the old password.
    if profile.profile_complete:
        return Response(
            {"detail": "Onboarding is already complete. Use Settings to change your profile."},
            status=403,
        )

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
