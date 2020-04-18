from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

class OrderDetailViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        user = request.data.get('userId', None)
        if user is not None:
            queryset = OrderDetail.objects.filter(user=user)
        else:
            return Response({"error": "Missing user id.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        queryset = queryset.values('id', 'status')
        return Response({"Response":{"order": queryset}, "status": 200}, status=status.HTTP_200_OK)

class OrderListViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        user = request.data.get('userId', None)
        if user is not None:
            queryset = OrderDetail.objects.filter(user=user)
        else:
            return Response({"error": "Missing user id.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        queryset = queryset.values('id', 'status')
        return Response({"order": queryset, "status": 200}, status=status.HTTP_200_OK)

class PlaceOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset
