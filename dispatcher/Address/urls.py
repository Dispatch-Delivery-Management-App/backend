from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'address', AddressViewSet, basename='address')

urlpatterns = router.urls
