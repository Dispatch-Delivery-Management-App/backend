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
        return Response({"message":"hello"}, status=status.HTTP_200_OK)