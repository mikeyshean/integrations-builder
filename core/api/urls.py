from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from integrations.urls import router as integrations_router

from . import views
from .views import CustomTokenObtainPairView

urlpatterns = [
    path("", views.get_routes),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(integrations_router.urls), name="integrations"),
]
