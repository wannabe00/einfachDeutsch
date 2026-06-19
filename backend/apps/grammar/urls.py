from rest_framework.routers import SimpleRouter

from .views import GrammarRuleViewSet

router = SimpleRouter()
router.register("grammar/rules", GrammarRuleViewSet, basename="grammarrule")

urlpatterns = router.urls
