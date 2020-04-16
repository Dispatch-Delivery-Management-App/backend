from rest_framework import serializers
from .models import *

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ('id','name', 'price', 'capacity')

class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ('id','name', 'price', 'capacity')
