"""Root URL configuration.

The /api/ routes are wired in brick 0.2 (DRF + CORS).
"""

from django.contrib import admin
from django.urls import include, path

from apps.accounts import views

from .views import api_root

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_root, name="api-root"),
    # Auth: login (username/password), logout, user, password reset (dj-rest-auth).
    # Account creation is OAuth-only (Google/GitHub) — see apps.accounts.urls.
    # Login is overridden FIRST so the brute-force throttle applies (AUDIT S3).
    path("api/auth/login/", views.ThrottledLoginView.as_view(), name="rest_login"),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.books.urls")),
    path("api/", include("apps.vocabulary.urls")),
    path("api/", include("apps.grammar.urls")),
    path("api/", include("apps.exercises.urls")),
    path("api/", include("apps.ai_assistant.urls")),
    path("api/", include("apps.recitation.urls")),
    path("api/", include("apps.videos.urls")),
    path("api/", include("apps.history.urls")),
    path("api/", include("apps.curriculum.urls")),
]
