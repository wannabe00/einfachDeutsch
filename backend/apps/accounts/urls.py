from django.urls import path

from . import views

urlpatterns = [
    path("accounts/set-level/", views.set_level, name="set-level"),
    path("accounts/placement-test/", views.placement_test, name="placement-test"),
    path("accounts/level-status/", views.level_status, name="level-status"),
    path("accounts/streak/", views.streak, name="streak"),
    path("accounts/profile/", views.update_profile, name="update-profile"),
    path("accounts/avatar/", views.upload_avatar, name="upload-avatar"),
    path("accounts/logout-all/", views.logout_all, name="logout-all"),
    path("accounts/deactivate/", views.deactivate_account, name="deactivate"),
    path("accounts/delete/", views.delete_account, name="delete-account"),
    path("accounts/reset-progress/", views.reset_progress, name="reset-progress"),
    path("accounts/export/", views.export_data, name="export-data"),
]
