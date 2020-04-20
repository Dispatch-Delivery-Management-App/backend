from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'shippingmethod-drone', DroneViewSet, basename='drone')
router.register(r'shippingmethod-robot', RobotViewSet, basename='robot')

urlpatterns = router.urls