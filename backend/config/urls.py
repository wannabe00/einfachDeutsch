"""Root URL configuration.

The /api/ routes are wired in brick 0.2 (DRF + CORS).
"""

from django.contrib import admin
from django.urls import include, path

from .views import api_root

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_root, name="api-root"),
    # Auth: login, logout, user, password reset (dj-rest-auth) + registration.
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.books.urls")),
    path("api/", include("apps.vocabulary.urls")),
    path("api/", include("apps.grammar.urls")),
    path("api/", include("apps.exercises.urls")),
    path("api/", include("apps.ai_assistant.urls")),
    path("api/", include("apps.recitation.urls")),
    path("api/", include("apps.videos.urls")),
]
