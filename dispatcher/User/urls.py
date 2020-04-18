from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UserViewSet, basename = "user")
router.register(r'user-profile', ProfileViewSet, basename = "profile")
urlpatterns = router.urls
