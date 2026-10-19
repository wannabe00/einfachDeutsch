"""Two-factor login with an authenticator app: set up, turn on, turn off, new
backup codes. Turning it on or off and new codes need the account password,
so a stolen token alone can't lock the owner out. The login step itself is in
`serializers.LoginSerializer` (Google/GitHub logins rely on their own 2FA)."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .. import totp
from .danger import _password_error


def second_factor_ok(profile, code: str) -> bool:
    """A current authenticator code (each usable once) or an unused backup code."""
    step = totp.matching_step(profile.totp_secret, code)
    if step is not None and (profile.totp_last_step is None or step > profile.totp_last_step):
        profile.totp_last_step = step
        profile.save(update_fields=["totp_last_step"])
        return True
    hashed = totp.hash_backup(code)
    if hashed in profile.totp_backup_codes:
        profile.totp_backup_codes = [h for h in profile.totp_backup_codes if h != hashed]
        profile.save(update_fields=["totp_backup_codes"])
        return True
    return False


def _new_backup_codes(profile) -> list[str]:
    codes = totp.new_backup_codes()
    profile.totp_backup_codes = [totp.hash_backup(c) for c in codes]
    return codes


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def setup(request):
    """A fresh secret to scan; it only counts once confirmed with `enable`."""
    profile = request.user.profile
    if profile.totp_enabled:
        return Response({"detail": "Two-factor login is already on."}, status=400)
    profile.totp_secret = totp.new_secret()
    profile.save(update_fields=["totp_secret"])
    return Response(
        {
            "secret": profile.totp_secret,
            "uri": totp.setup_uri(profile.totp_secret, request.user.username),
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def enable(request):
    """Turn it on with a first code from the app; answers the backup codes, once."""
    error = _password_error(request)
    if error:
        return error
    profile = request.user.profile
    if profile.totp_enabled or not profile.totp_secret:
        return Response({"detail": "Start the setup first."}, status=400)
    step = totp.matching_step(profile.totp_secret, str(request.data.get("code") or ""))
    if step is None:
        return Response({"detail": "That code isn't right. Try the newest one."}, status=400)
    profile.totp_enabled = True
    profile.totp_last_step = step
    codes = _new_backup_codes(profile)
    profile.save()
    return Response({"backup_codes": codes})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def disable(request):
    error = _password_error(request)
    if error:
        return error
    profile = request.user.profile
    profile.totp_enabled = False
    profile.totp_secret = ""
    profile.totp_backup_codes = []
    profile.totp_last_step = None
    profile.save()
    return Response({"detail": "Two-factor login is off."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def backup_codes(request):
    """Replace the backup codes (the old ones stop working)."""
    error = _password_error(request)
    if error:
        return error
    profile = request.user.profile
    if not profile.totp_enabled:
        return Response({"detail": "Two-factor login is off."}, status=400)
    codes = _new_backup_codes(profile)
    profile.save(update_fields=["totp_backup_codes"])
    return Response({"backup_codes": codes})
