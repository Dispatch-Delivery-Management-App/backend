from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'tracking', TrackingViewSet, basename='tracking')

urlpatterns = router.urls
