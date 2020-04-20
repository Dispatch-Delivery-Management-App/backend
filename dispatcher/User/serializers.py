from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'type', 'email', 'password', 'firstname', 'lastname')


class UserLoginSerializer(serializers.ModelSerializer):
    """
    用户登录序列化类
    """
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)
    token = serializers.CharField(required=False, max_length=1024)

    class Meta:
        model = User
        fields = ('id', 'username', 'type', 'email', 'password', 'firstname', 'lastname', 'token')
