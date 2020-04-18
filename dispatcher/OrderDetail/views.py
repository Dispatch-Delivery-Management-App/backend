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
        user = request.data.get('userId', None)
        if user is not None:
            # queryset = OrderDetail.objects.filter(user=user)
            sql = "SELECT * FROM OrderDetail_orderdetail O "\
                  "JOIN(SELECT id AS  from_id, firstname AS From_FirstName, lastname AS From_LastName, " \
                  "street AS From_Street, city AS From_City, state AS From_State, zipcode AS From_Zipcode "\
                  "FROM Address_address) A "\
                  "ON O.from_address_id = A.from_id "\
                  "JOIN(SELECT id AS to_id, firstname AS To_FirstName, lastname AS To_LastName, " \
                  "street AS To_Street, city AS To_City, state AS To_State, zipcode As To_Zipcode " \
                  "FROM Address_address) A2 " \
                  "ON O.to_address_id = A2.to_id " \
                  "WHERE O.user_id = {};".format(user)
            res = executeSQL(sql)
        else:
            return Response({"status": 400, "error": "Missing user id."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": 200, "Response":{"order": res}}, status=status.HTTP_200_OK)

class OrderListViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        user = request.data.get('userId', None)
        if user is not None:
            sql = "SELECT OrderDetail_orderdetail.id, category, status, lastname " \
                  "FROM OrderDetail_orderdetail " \
                  "JOIN Address_address A2 ON OrderDetail_orderdetail.to_address_id = A2.id " \
                  "WHERE OrderDetail_orderdetail.user_id = {};"\
                .format(user)
            res = executeSQL(sql)
        else:
            return Response({"error": "Missing user id.", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"order": res, "status": 200}, status=status.HTTP_200_OK)

class PlaceOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset
