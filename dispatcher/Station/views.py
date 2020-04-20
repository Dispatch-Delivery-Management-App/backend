from .serializers import *
from rest_framework import viewsets, status
from django.http import JsonResponse

class StationViewSet(viewsets.ModelViewSet):
    serializer_class = StationSerializer

    def get_queryset(self):
        queryset = Station.objects.all()
        return queryset


class StationDroneViewSet(viewsets.ModelViewSet):
    serializer_class = StationDroneSerializer

    def get_queryset(self):
        queryset = Station.objects.all()
        return queryset

class StationRobotViewSet(viewsets.ModelViewSet):
    serializer_class = StationRobotSerializer

    def get_queryset(self):
        queryset = Station.objects.all()
        return queryset
