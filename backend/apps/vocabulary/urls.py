from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ActivityView, StatsView, WordViewSet

router = SimpleRouter()
router.register(r"vocabulary/words", WordViewSet, basename="word")

urlpatterns = router.urls + [
    path("stats/", StatsView.as_view(), name="stats"),
    path("stats/activity/", ActivityView.as_view(), name="stats-activity"),
]
