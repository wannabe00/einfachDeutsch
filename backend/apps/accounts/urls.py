from django.urls import path

from . import views

urlpatterns = [
    # Social login (SPA posts the OAuth `code` → DRF token).
    path("auth/google/", views.GoogleLogin.as_view(), name="google-login"),
    path("auth/github/", views.GitHubLogin.as_view(), name="github-login"),
    path("accounts/complete-onboarding/", views.complete_onboarding, name="complete-onboarding"),
    path("accounts/set-level/", views.set_level, name="set-level"),
    path("accounts/placement-test/", views.placement_test, name="placement-test"),
    path("accounts/streak/", views.streak, name="streak"),
    path("accounts/premium/", views.premium_status, name="premium-status"),
    path("billing/checkout/", views.checkout, name="billing-checkout"),
    path("billing/confirm/", views.confirm, name="billing-confirm"),
    path("billing/portal/", views.portal, name="billing-portal"),
    path("billing/webhook/", views.webhook, name="billing-webhook"),
    path("accounts/profile/", views.update_profile, name="update-profile"),
    path("accounts/avatar/", views.upload_avatar, name="upload-avatar"),
    path("accounts/logout-all/", views.logout_all, name="logout-all"),
    path("accounts/2fa/setup/", views.two_factor_setup, name="2fa-setup"),
    path("accounts/2fa/enable/", views.two_factor_enable, name="2fa-enable"),
    path("accounts/2fa/disable/", views.two_factor_disable, name="2fa-disable"),
    path("accounts/2fa/backup-codes/", views.two_factor_backup_codes, name="2fa-backup-codes"),
    path("accounts/deactivate/", views.deactivate_account, name="deactivate"),
    path("accounts/delete/", views.delete_account, name="delete-account"),
    path("accounts/reset-progress/", views.reset_progress, name="reset-progress"),
    path("accounts/export/", views.export_data, name="export-data"),
    path("accounts/client-ip/", views.client_ip, name="client-ip"),
]
