from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'orderdetail', OrderDetailViewSet, basename='orderdetail')
router.register(r'orderlist', OrderListViewSet, basename='orderlist')
router.register(r'placeorder', PlaceOrderViewSet, basename='placeorder')

urlpatterns = router.urls
