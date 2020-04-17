from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    def get_queryset(self):
        queryset = Address.objects.all()
        return queryset
