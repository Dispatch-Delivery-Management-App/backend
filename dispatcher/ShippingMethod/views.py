from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response

class DroneViewSet(viewsets.ModelViewSet):
    serializer_class = DroneSerializer
    def get_queryset(self):
        queryset = Drone.objects.all()
        return queryset

    def create(self, request):
        name = request.data.get('name')
        price = request.data.get('price')
        capacity = request.data.get('capacity')
        instance = Drone(name=name,price=price,capacity=capacity)
        instance.save()
        return Response({"status":201, "response": "Success"}, status=status.HTTP_201_CREATED)

class RobotViewSet(viewsets.ModelViewSet):
    serializer_class = RobotSerializer

    def get_queryset(self):
        queryset = Robot.objects.all()
        return queryset

    def create(self, request):
        name = request.data.get('name')
        price = request.data.get('price')
        capacity = request.data.get('capacity')
        instance = Robot(name=name,price=price,capacity=capacity)
        instance.save()
        return Response({"status":201, "response": "Success"}, status=status.HTTP_201_CREATED)
