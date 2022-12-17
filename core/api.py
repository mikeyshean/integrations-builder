from django.urls import re_path, include
from integrations.urls import router as integrations_router

urlpatterns = [
    re_path(r"^", include(integrations_router.urls)),
]