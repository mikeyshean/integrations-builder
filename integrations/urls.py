from rest_framework.routers import SimpleRouter
from integrations.views import IntegrationsViewSet


router = SimpleRouter(trailing_slash=False)
router.register(r"integrations", IntegrationsViewSet, basename="integrations")