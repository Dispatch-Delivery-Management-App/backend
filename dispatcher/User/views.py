from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

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
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if username is None:
            return Response({"error": "No user name.", 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
        if password is None:
            return Response({"error": "No password.", 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User name not found.', 'status': 404}, status=status.HTTP_404_NOT_FOUND)
        else:
            if user.password == password:
                return Response(request.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password.', 'status': 401}, status=status.HTTP_401_UNAUTHORIZED)