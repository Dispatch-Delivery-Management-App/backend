from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'orderdetail', OrderDetailViewSet, basename='orderdetail')
router.register(r'orderlist', OrderListViewSet, basename='orderlist')
router.register(r'placeorder', PlaceOrderViewSet, basename='placeorder')
router.register(r'search', SearchOrderViewSet, basename='search')
router.register(r'map', OrderMapViewSet, basename='map')
router.register(r'orderplan', OrderPlanViewSet, basename='orderplan')
router.register(r'feedback', FeedbackViewSet, basename='feedback')

urlpatterns = router.urls
