from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'tracking', StationViewSet, basename='tracking')
router.register(r'tracking', StationDroneViewSet, basename='tracking')
router.register(r'tracking', StationRobotViewSet, basename='tracking')

urlpatterns = router.urls