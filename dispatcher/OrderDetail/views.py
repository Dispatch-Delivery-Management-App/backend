from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from .utils import *
import datetime

from Address.models import Address
from Station.models import Station
from Tracking.models import Tracking
from OrderDetail.models import OrderDetail

import json

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
        user = request.data.get('userId', None)
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

    def create(self,request):
        print("in create")
        user_id = request.data.get('user_id', None)
        if user_id is None: return Response({"error": "Missing user id.", "status": 400},
                                            status=status.HTTP_400_BAD_REQUEST)
        try:
            self.get_orderdetail(request)
            return Response({"response": {"status": 200}}, status=status.HTTP_200_OK)
        except:
            print("Unable to place this order")
            return Response({"error": "Internal Error Happened", "status": 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_orderdetail(self,request):
        user_id = self.request.data.get("user_id")
        print("in save detail")
        (from_address_id, to_address_id)= self.verify_address_id(request, user_id)
        print(from_address_id, to_address_id)
        station= request.data.get('station')
        tracking= request.data.get('tracking')
        try:
            po = OrderDetail(user=user_id, from_address=from_address_id, to_address=to_address_id, station=station,tracking=tracking)
            po.save()
        except:
            print("Unable to save orderdetail model")
            raise()
        return None


    def verify_address_id(self, request, user_id):
        print("In verify_address_id")
        faddr = request.data.get('fromAddress', None)
        taddr = request.data.get('toAddress', None)

        faddr_id = self.check_address_id(faddr, user_id)
        taddr_id = self.check_address_id(taddr, user_id)
        print("in verify_address_id",faddr_id, taddr_id)
        return faddr_id, taddr_id

    #If address id not exist, insert id
    def check_address_id(self, addr, user_id):
        print("check_address_id")
        if addr is None:
            raise ValueError
        try:
            if "addr_id" in addr: return addr["addr_id"]
            print("not in")
            cur_id = self.get_address_id(addr["firstname"],
                                    addr["lastname"], addr["street"], addr["city"], addr["state"], addr["zipcode"])
            if cur_id is None:
                cur_id = self.insert_new_address(addr["firstname"],
                                    addr["lastname"], addr["street"], addr["city"], addr["state"], addr["zipcode"])
            return cur_id
        except:
            print("Unable to get address Id")

    #check if address is already in DB
    def get_address_id(self, fname, lname, street, city, state, zipcode):
        print("in get_address_id")
        print(fname, lname, street, city, state, zipcode)
        addr = Address.objects.filter(firstname=fname, lastname=lname, street=street, city=city,
                                      state=state,zipcode=zipcode).values_list('id', flat=True)
        print(addr)

        return None if not addr else addr[0]

    #insert new address to DB
    def insert_new_address(self,fname, lname, street, city, state, zipcode):
        print("in insert_new_address")
        addr = Address(firstname=fname, lastname=lname, street=street, city=city,state=state,zipcode=zipcode)
        addr.save()
        new_addr = Address.objects.filter(firstname=fname, lastname=lname, street=street, city=city, state=state,
                                      zipcode=zipcode).values_list('id', flat=True)
        return new_addr[0]