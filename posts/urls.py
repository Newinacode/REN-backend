from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.post import PostViewSet

router = DefaultRouter()
router.register(r"post", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]
