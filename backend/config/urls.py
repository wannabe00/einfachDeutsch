"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path

from apps.accounts import views

from .views import admin_login, api_root

urlpatterns = [
    # Before the admin's own URLs, so its login gets the attempt limit.
    path("admin/login/", admin_login, name="admin-login"),
    path("admin/", admin.site.urls),
    path("api/", api_root, name="api-root"),
    # Auth: login (username/password), logout, user, password reset (dj-rest-auth).
    # Accounts are only created through Google or GitHub; see apps.accounts.urls.
    # Login and password reset/change are overridden FIRST so their throttles apply.
    path("api/auth/login/", views.ThrottledLoginView.as_view(), name="rest_login"),
    path(
        "api/auth/password/reset/",
        views.ThrottledPasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "api/auth/password/reset/confirm/",
        views.ThrottledPasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path(
        "api/auth/password/change/",
        views.ThrottledPasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.books.urls")),
    path("api/", include("apps.vocabulary.urls")),
    path("api/", include("apps.grammar.urls")),
    path("api/", include("apps.ai_assistant.urls")),
    path("api/", include("apps.talk.urls")),
    path("api/", include("apps.videos.urls")),
    path("api/", include("apps.history.urls")),
    path("api/", include("apps.curriculum.urls")),
]
