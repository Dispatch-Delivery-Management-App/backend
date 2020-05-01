from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

from ShippingMethod.models import *

class StationViewSet(viewsets.ModelViewSet):
    serializer_class = StationSerializer

    def get_queryset(self):
        queryset = Station.objects.all()
        return queryset

    def create(self, request):
        name = request.data.get('name', None)
        street = request.data.get('street', None)
        city = request.data.get('city', None)
        state = request.data.get('state', None)
        zipcode = request.data.get('zipcode', None)
        total_rating = request.data.get('total_rating', None)
        rating_count = request.data.get('rating_count', None)
        rating = request.data.get('rating', None)

        instance = Station(name=name, street=street, city=city, state=state, zipcode=zipcode, total_rating=total_rating, rating_count=rating_count, rating=rating)
        instance.save()
        return Response({"status":201, "response": "Success"}, status=status.HTTP_201_CREATED)

class StationDroneViewSet(viewsets.ModelViewSet):
    serializer_class = StationDroneSerializer

    def get_queryset(self):
        queryset = StationDrone.objects.all()
        return queryset

    def create(self, request):
        station_id = request.data.get('station_id', 1)
        drone_id = request.data.get('drone_id', None)
        instance = StationDrone(station=Station.objects.get(id=station_id), drone=Drone.objects.get(id=drone_id),status=0)
        instance.save()
        return Response({"status":201, "response": "Success"}, status=status.HTTP_201_CREATED)

class StationRobotViewSet(viewsets.ModelViewSet):
    serializer_class = StationRobotSerializer

    def get_queryset(self):
        queryset = StationRobot.objects.all()
        return queryset

    def create(self, request):
        station_id = request.data.get('station_id', 1)
        robot_id = request.data.get('robot_id', None)
        instance = StationRobot(station=Station.objects.get(id=station_id), robot=Robot.objects.get(id=robot_id),status=0)
        instance.save()
        return Response({"status":201, "response": "Success"}, status=status.HTTP_201_CREATED)
