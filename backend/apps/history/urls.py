from rest_framework.routers import SimpleRouter

from .views import CustomLessonViewSet, HistoryLessonViewSet

router = SimpleRouter()
# Registered first so "history/custom/" isn't read as a lesson id.
router.register("history/custom", CustomLessonViewSet, basename="history-custom")
router.register("history", HistoryLessonViewSet, basename="history")

urlpatterns = router.urls
