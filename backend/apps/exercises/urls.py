from rest_framework.routers import SimpleRouter

from .views import ExerciseViewSet

router = SimpleRouter()
router.register("exercises", ExerciseViewSet, basename="exercise")

urlpatterns = router.urls
