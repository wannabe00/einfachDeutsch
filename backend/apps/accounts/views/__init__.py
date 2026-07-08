"""Accounts views, split by concern (AUDIT R5):

- leveling.py — set level, placement test, progression, streak
- profile.py  — profile updates, avatar, onboarding, data export
- social.py   — Google/GitHub code exchange, throttled login
- danger.py   — logout-all, deactivate, delete, reset progress

Everything is re-exported here so `from . import views` keeps working.
"""

from .danger import deactivate_account, delete_account, logout_all, reset_progress
from .leveling import level_status, placement_test, set_level, streak
from .profile import complete_onboarding, export_data, update_profile, upload_avatar
from .social import GitHubLogin, GoogleLogin, ThrottledLoginView

__all__ = [
    "GitHubLogin",
    "GoogleLogin",
    "ThrottledLoginView",
    "complete_onboarding",
    "deactivate_account",
    "delete_account",
    "export_data",
    "level_status",
    "logout_all",
    "placement_test",
    "reset_progress",
    "set_level",
    "streak",
    "update_profile",
    "upload_avatar",
]
