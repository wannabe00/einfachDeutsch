"""Root URL configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from apps.accounts import views

from .admin_login import admin_login
from .views import api_root

urlpatterns = [
    # The admin lives at a secret path in production (ADMIN_URL). Its login comes
    # first so it gets the attempt limit and the authenticator code.
    path(f"{settings.ADMIN_URL}login/", admin_login, name="admin-login"),
    path(settings.ADMIN_URL, admin.site.urls),
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
