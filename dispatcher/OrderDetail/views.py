from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from .utils import *


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

    def create(self, request):
        user = request.data.get('user_id', None)
        if user is not None:
            sql = "SELECT OrderDetail_orderdetail.id, category, status, lastname FROM OrderDetail_orderdetail JOIN Address_address A2 ON OrderDetail_orderdetail.to_address_id = A2.id WHERE OrderDetail_orderdetail.user_id = {};".format(user)
            res = executeSQL(sql)
        else:
            return Response({"error": "Missing user id.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"response": {"order": res, "status": 200}}, status=status.HTTP_200_OK)

class PlaceOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset
