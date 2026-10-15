from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ActivityView, PublicStatsView, SavedWordViewSet, StatsView, WordViewSet

router = SimpleRouter()
router.register(r"vocabulary/words", WordViewSet, basename="word")
router.register(r"vocabulary/saved", SavedWordViewSet, basename="saved-word")

urlpatterns = router.urls + [
    path("stats/", StatsView.as_view(), name="stats"),
    path("stats/activity/", ActivityView.as_view(), name="stats-activity"),
    path("stats/public/", PublicStatsView.as_view(), name="stats-public"),
]
