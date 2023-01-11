from rest_framework.routers import SimpleRouter

from mappers.views import JsonMapperViewSet

router = SimpleRouter(trailing_slash=False)
router.register("mappers/json", JsonMapperViewSet, basename="json-mapper")
