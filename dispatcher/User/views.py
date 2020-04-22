from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

from .utils import executeSQL


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def retrieve(self, request, pk=None):
        #queryset = User.objects.all()
        return Response({"message": "hello"}, status=status.HTTP_200_OK)

class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if username is None:
            return Response({"error": "No user name.", 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        if password is None:
            return Response({"error": "Wrong password.", 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        sql = "SELECT * FROM User_user U " \
              "WHERE U.username = '{0}' AND U.password = '{1}';".format(username, password)
        res = executeSQL(sql)
        if res is None:
            return Response({"error": "Invalid user.", 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)