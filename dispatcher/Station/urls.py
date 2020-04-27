
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'station', StationViewSet, basename='station')
router.register(r'station-drone', StationDroneViewSet, basename='stationdrone')
router.register(r'station-robot', StationRobotViewSet, basename='stationrobot')

urlpatterns = router.urls
