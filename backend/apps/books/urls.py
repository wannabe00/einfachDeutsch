from rest_framework.routers import SimpleRouter

from .views import BookViewSet

router = SimpleRouter()
router.register("books", BookViewSet, basename="book")

urlpatterns = router.urls
