from rest_framework.routers import SimpleRouter

from .views import HistoryLessonViewSet

router = SimpleRouter()
router.register("history", HistoryLessonViewSet, basename="history")

urlpatterns = router.urls
