from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from .utils import *


class OrderDetailViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        user = request.data.get('user_id', None)
        if user is not None:
            # queryset = OrderDetail.objects.filter(user=user)
            sql = "SELECT * FROM OrderDetail_orderdetail O "\
                  "JOIN(SELECT id AS  from_id, firstname AS from_firstname, lastname AS from_lastname, " \
                  "street AS from_street, city AS from_city, state AS from_state, zipcode AS from_zipcode "\
                  "FROM Address_address) A "\
                  "ON O.from_address_id = A.from_id "\
                  "JOIN(SELECT id AS to_id, firstname AS to_firstname, lastname AS to_lastname, " \
                  "street AS to_street, city AS to_city, state AS to_state, zipcode As to_zipcode " \
                  "FROM Address_address) A2 " \
                  "ON O.to_address_id = A2.to_id " \
                  "WHERE O.user_id = {};".format(user)
            res = executeSQL(sql)
        else:
            return Response({"status": 400, "error": "Missing user id."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": 200, "response": res}, status=status.HTTP_200_OK)

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
        return Response({"response": res, "status": 200}, status=status.HTTP_200_OK)


class PlaceOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset
