from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'address', AddressViewSet, basename='address')
router.register(r'address-list', AddressListViewSet, basename="addresslist")

urlpatterns = router.urls
