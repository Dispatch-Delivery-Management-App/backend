from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

class OrderDetailViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

class OrderListViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

class PlaceOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset
