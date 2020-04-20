from django.conf.urls import url
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

router.register(r'user', UserViewSet, basename="user")
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = router.urls
