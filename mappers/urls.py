from rest_framework.routers import SimpleRouter

from mappers.views import JsonMapperViewSet, ModelViewSet

router = SimpleRouter(trailing_slash=False)
router.register("mappers/json", JsonMapperViewSet, basename="json-mapper")
router.register("models", ModelViewSet, basename="models")
