from .serializers import *
from rest_framework import viewsets


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

