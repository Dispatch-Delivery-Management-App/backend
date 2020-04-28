from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'tracking', TrackingViewSet, basename='tracking')
router.register(r'notification', NotificationViewSet, basename='notification')
router.register(r'token', TokenViewSet, basename='token')

urlpatterns = router.urls
