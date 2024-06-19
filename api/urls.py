from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CharacterViewSet, TeamViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"characters", CharacterViewSet)
router.register(r"team", TeamViewSet, basename="team")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
