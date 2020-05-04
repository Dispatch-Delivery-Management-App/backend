from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

from .utils import executeSQL


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    def get_queryset(self):
        queryset = Address.objects.all()
        return queryset

    # Post
    def create(self, request):
        address_id = request.data.get('address_id', None)
        if address_id is not None:
            # queryset = Address.objects.filter(address_id = address_id)
            sql = "SELECT * FROM \"Address_address\" A "\
                  "WHERE A.id = {};".format(address_id)
            res = executeSQL(sql)
        else:
            return Response({"status": 400, "error": "Missing address id."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": 200, "response": res}, status=status.HTTP_200_OK)

class AddressListViewSet(viewsets.ModelViewSet):
    serializer_class = AddressListSerializer

    def get_queryset(self):
        queryset = AddressList.objects.all()
        return queryset

    def create(self, request):
        user = request.data.get('user_id', None)

        if user is None:
            return Response({"status": 400, "error": "Missing user id."}, status=status.HTTP_400_BAD_REQUEST)

        sql = "SELECT * FROM \"Address_addresslist\" L " \
              "JOIN \"Address_address\" A "\
              "ON L.address_id = A.id "\
              "WHERE user_id = {};".format(user)
        res = executeSQL(sql)
        return Response({"status": 200, "response": res}, status=status.HTTP_200_OK)
