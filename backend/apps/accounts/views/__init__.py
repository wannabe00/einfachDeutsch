"""Accounts views, split by concern:

- leveling.py: set level, placement test, streak
- profile.py: profile updates, avatar, onboarding, data export
- social.py: Google/GitHub code exchange, throttled login
- danger.py: logout everywhere, deactivate, delete, reset progress
- diagnostics.py: staff-only client address check (throttle keys)
- premium.py: premium status
- billing.py: Stripe Checkout, Customer Portal, webhook
- twofactor.py: authenticator-app two-factor login

Everything is re-exported so `from . import views` keeps working.
"""

from .billing import checkout, confirm, portal, webhook
from .danger import deactivate_account, delete_account, logout_all, reset_progress
from .diagnostics import client_ip
from .leveling import placement_test, set_level, streak
from .premium import premium_status
from .profile import complete_onboarding, export_data, update_profile, upload_avatar
from .social import (
    GitHubLogin,
    GoogleLogin,
    ThrottledLoginView,
    ThrottledPasswordChangeView,
    ThrottledPasswordResetConfirmView,
    ThrottledPasswordResetView,
)
from .twofactor import backup_codes as two_factor_backup_codes
from .twofactor import disable as two_factor_disable
from .twofactor import enable as two_factor_enable
from .twofactor import setup as two_factor_setup

__all__ = [
    "client_ip",
    "two_factor_backup_codes",
    "two_factor_disable",
    "two_factor_enable",
    "two_factor_setup",
    "GitHubLogin",
    "GoogleLogin",
    "ThrottledLoginView",
    "ThrottledPasswordChangeView",
    "ThrottledPasswordResetConfirmView",
    "ThrottledPasswordResetView",
    "complete_onboarding",
    "premium_status",
    "checkout",
    "confirm",
    "portal",
    "webhook",
    "deactivate_account",
    "delete_account",
    "export_data",
    "logout_all",
    "placement_test",
    "reset_progress",
    "set_level",
    "streak",
    "update_profile",
    "upload_avatar",
]
