import re
import sys

import requests

from Address.models import Address
from OrderDetail.models import OrderDetail
from OrderDetail.serializers import OrderDetailSerializer
from OrderDetail.utils import GOOGLEMAP_BASE_URL
from Station.models import Station
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

from .utils import executeSQL


class DroneViewSet(viewsets.ModelViewSet):
    serializer_class = DroneSerializer
    def get_queryset(self):
        queryset = Drone.objects.all()
        return queryset

class RobotViewSet(viewsets.ModelViewSet):
    serializer_class = RobotSerializer

    def get_queryset(self):
        queryset = Robot.objects.all()
        return queryset

class OrderPlanViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    def get_queryset(self):
        queryset = OrderDetail.objects.all()
        return queryset

    def create(self, request):
        toAddress = request.data.get('to_address')
        fromAddress = request.data.get('from_address')
        capacity = request.data.get('capacity')

        if toAddress is None or fromAddress is None:
            return Response({"status": 400, "error": "Missing order id."}, status=status.HTTP_400_BAD_REQUEST)

        toAddressObj = Address.objects.get(id=toAddress)

        fromAddressObj = Address.objects.get(id=fromAddress)
        from_address_str = fromAddressObj.street + '+' + fromAddressObj.city + '+' + fromAddressObj.state
        to_address_Str = toAddressObj.street + '+' + toAddressObj.city + '+' + toAddressObj.state

        #time lowest
        print(toAddressObj.state)
        sql = "SELECT * FROM \'Station_station\' S " \
              "WHERE S.state = '{0}' ".format(toAddressObj.state)
        instance = executeSQL(sql)
        print(instance)
        globalDistance = 1000000.0
        globalStationId = -1
        for station in instance:
            state = station.get('state')
            city = station.get('city')
            street = station.get('street')
            id = station.get('id')
            station_str = street + '+' + city + '+' + state
            PARAMS = {
                'origin' : station_str,
                'destination' : to_address_Str,
                'waypoints' : from_address_str,
                'mode' : 'driving',
                'key': 'AIzaSyDJ7sVPTcdaIA2If4BPN43JqXnio8qfjyQ'
            }
            data = requests.get(GOOGLEMAP_BASE_URL, PARAMS).json()
            if data['status'] != 'OK':
                return Response({"status": 400, "error": "Address has error"}, status=status.HTTP_400_BAD_REQUEST)
            curDistance = re.findall(r"\d+\.?\d*",data['routes'][0]['legs'][0]['distance']['text'])
            if float(curDistance[0]) < globalDistance:
                globalDistance = float(curDistance[0])
                globalStationId = id
        fastTime = int(globalDistance / 1.5)
        fastMethod = "drone"

        #price lowest

        lowestPriceMethod = "drone"
        droneObj = Drone.objects.first()
        droneCapacity = float(getattr(droneObj, 'capacity'))
        dronePrice = int(getattr(droneObj, 'price'))
        robotObj = Robot.objects.first()
        robotCapacity = float(getattr(robotObj, 'capacity'))
        robotPrice = int(getattr(robotObj, 'price'))
        rating = Station.objects.all()
        ratingList = rating.values_list('rating', flat=True)
        totalRating = float(ratingList[0])
        cheapCost = sys.maxsize
        fastCost = float(capacity / droneCapacity) * dronePrice
        fastAmount = int((capacity / droneCapacity) + 1)
        CheapAmount = 0
        if (capacity / droneCapacity + 1) * dronePrice < (capacity / robotCapacity + 1) * robotPrice:
            lowestPriceMethod = "drone"
            cheapCost = (capacity / droneCapacity + 1) * dronePrice
            cheapAmount = int(capacity / droneCapacity + 1)
            cheapTime = fastTime + 10
        else:
            lowestPriceMethod = "robot"
            cheapCost = (capacity / robotCapacity + 1) * robotPrice
            cheapAmount = int(capacity / robotCapacity + 1)
            cheapTime = fastTime + 10
        return Response([{"type": 2,
                          "station": globalStationId,
                          "fee": fastCost,
                          "duration": fastTime,
                          "shipping_method": fastMethod,
                          "amount": fastAmount,
                          "rating": totalRating},
                          {"type":1,
                           "station": globalStationId,
                           "fee":cheapCost,
                           "duration": cheapTime,
                           "shipping_method": lowestPriceMethod,
                           "amount": cheapAmount,
                           "rating":totalRating}])

