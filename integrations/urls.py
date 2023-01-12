from rest_framework.routers import SimpleRouter

from integrations.views import (
    EndpointViewSet,
    IntegrationCategoriesViewSet,
    IntegrationsViewSet,
)

router = SimpleRouter(trailing_slash=False)
router.register(
    r"integration/categories/", IntegrationCategoriesViewSet, basename="categories"
)
router.register(r"integrations", IntegrationsViewSet, basename="integrations")


endpoint_router = SimpleRouter(trailing_slash=False)
endpoint_router.register(r"endpoints", EndpointViewSet, basename="endpoints")
