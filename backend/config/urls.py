"""Root URL configuration.

The /api/ routes are wired in brick 0.2 (DRF + CORS).
"""

from django.contrib import admin
from django.urls import include, path

from .views import api_root

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_root, name="api-root"),
    path("api/", include("apps.books.urls")),
    path("api/", include("apps.vocabulary.urls")),
    path("api/", include("apps.grammar.urls")),
    path("api/", include("apps.exercises.urls")),
    path("api/", include("apps.ai_assistant.urls")),
]
