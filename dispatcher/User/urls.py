from django.conf.urls import url
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

router.register(r'user-login', LoginViewSet, basename = "login")
router.register(r'user-signup', SignUpViewSet, basename = "signup")

urlpatterns = router.urls
