from rest_framework.routers import SimpleRouter

from integrations.views import IntegrationCategoriesViewSet, IntegrationsViewSet

router = SimpleRouter(trailing_slash=False)
router.register(
    "integration-categories/", IntegrationCategoriesViewSet, basename="categories"
)
router.register("integrations", IntegrationsViewSet, basename="integrations")
