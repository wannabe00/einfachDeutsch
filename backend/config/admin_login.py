"""The Django admin's login: the app's attempt limit, and the authenticator
code. Staff must have two-factor login on to use the admin (Settings >
Security), unless ADMIN_REQUIRE_2FA is off (it is with DEBUG)."""

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.http import HttpResponse


class TwoFactorAdminLoginForm(AdminAuthenticationForm):
    code = forms.CharField(
        label="Authenticator code",
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "one-time-code", "inputmode": "numeric"}),
    )

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)  # active staff only
        from apps.accounts.views.twofactor import second_factor_ok

        profile = getattr(user, "profile", None)
        if profile is None or not profile.totp_enabled:
            if settings.ADMIN_REQUIRE_2FA:
                raise forms.ValidationError(
                    "Turn on two-factor login in the app (Settings > Security) to use the admin.",
                    code="no_2fa",
                )
            return
        if not second_factor_ok(profile, self.cleaned_data.get("code") or ""):
            raise forms.ValidationError(
                "Enter the current code from your authenticator app.", code="bad_code"
            )


admin.site.login_form = TwoFactorAdminLoginForm


def admin_login(request, **kwargs):
    """Admin login with the same per-IP attempt limit as the app's login."""
    from apps.accounts.throttles import LoginThrottle

    if request.method == "POST" and not LoginThrottle().allow_request(request, None):
        return HttpResponse("Too many login attempts. Try again in a minute.", status=429)
    return admin.site.login(request, **kwargs)
